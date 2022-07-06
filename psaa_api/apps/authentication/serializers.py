from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from psaa_api.utils.password_validators import get_password_policy_errors
from psaa_api.utils.baseserializer import BaseSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='user with this email already exists'
            )
        ]
    )
    password = serializers.CharField(
        max_length=250,
        write_only=True,
        allow_null=True,
        allow_blank=True,
        required=True
    )

    def validate_password(self, value):
        errors = get_password_policy_errors(value)
        if errors:
            raise serializers.ValidationError(errors)
        return value

    username = serializers.RegexField(
        regex='^(?!.*\.)[A-Za-z\d\-\_\ ]+$',
        required=True,
        # validators=[
        #     UniqueValidator(
        #         queryset=User.objects.all(),
        #         message='user with this username already exists',
        #     )
        # ],
        error_messages={
            'invalid': 'Username can only contain letters, numbers, underscores, and hyphens',
            'required': 'Username is a required field'
        }
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        max_length=255, allow_blank=True)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(
        max_length=128, write_only=True, allow_blank=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if not email and not password:
            resp = {
                'email': 'An email address is required to log in.',
                'password': 'A password is required to log in.'
            }
            raise serializers.ValidationError(resp)

        if not email:
            resp = {
                'email': 'An email address is required to log in.'
            }
            raise serializers.ValidationError(resp)
        if not password:
            resp = {
                'password': 'A password is required to log in.'
            }
            raise serializers.ValidationError(resp)

        user = authenticate(username=email, password=password)

        if user is None:
            resp = {
                'credentials': 'Wrong email or password.'
            }
            raise serializers.ValidationError(resp)

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
        }


class AuthSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'token', 'password')

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class UsersSerializer(BaseSerializer):
    """Handles serialization and deserialization of User objects."""

    def __init__(self, *args, **kwargs):
        super(UsersSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'phone_number', 'is_active',
            'is_staff', 'created_at', 'updated_at'
        )
