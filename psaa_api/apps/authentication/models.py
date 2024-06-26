from pyexpat import model
from unicodedata import name
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

# from psaa_api.apps.schools.models import School


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser powers.

        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    phone_number = models.CharField(default='', max_length=100)
    national_id = models.CharField(default='', max_length=100)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def token(self):
        """
        This method allows us to get the jwt token by calling the user.token
        method.
        """
        return self.generate_jwt_token()

    def generate_jwt_token(self):
        """
        This method allows the creation of a jwt token. User's username and
        email are used in the encoding of the token.
        The token is generated during sign up.
        """
        user_details = {'email': self.email,
                        'username': self.username}
        token = jwt.encode(
            {
                'user_data': user_details,
                'exp': datetime.now() + timedelta(hours=720)
            }, settings.SECRET_KEY, algorithm='HS256'
        )
        return token

    def get_roles(self):
        """Get roles of the user"""
        permissions = Permission.objects.filter(user=self.pk).values()
        data = []
        for permission in permissions:
            role = Role.objects.get(
                pk=permission['role_id']
            )
            role = {
                "id": role.id,
                "name": role.name,
            }
            data.append(role)
        return data


class Role(models.Model):
    """
    Roles models
    """
    name = models.CharField(
        unique=True, null=False,
        blank=False, max_length=100
    )
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "roles"


class Permission(models.Model):
    """
    Permissions models to allow users based on roles.
    """
    role = models.ForeignKey(
        Role, related_name='permission_role',
        on_delete=models.CASCADE, null=False
    )
    user = models.ForeignKey(
        User, related_name='permission_user',
        on_delete=models.CASCADE, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "permissions"

    def get_role(self):
        """Get roles of the user"""
        return {
            'id': self.role.id,
            'name': self.role.name,
            'description': self.role.description,
        }

    def get_user(self):
        """Get the user"""
        return {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
