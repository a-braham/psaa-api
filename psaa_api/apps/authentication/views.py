from email import message
from requests import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import (RegistrationSerializer,
                          LoginSerializer, UserSerializer)
from psaa_api.utils.authentication_handlers import AuthTokenHandler
from .renderers import UserJSONRenderer

User = get_user_model()


class RegistrationAPI(GenericAPIView):
    """Sign up api view"""

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=data.get("email"))
        token = AuthTokenHandler.create_auth_token(user)
        data["token"] = token.key
        message = {
            "user": {
                "email": serializer.data.get('email'),
                "username": serializer.data.get("username"),
                "token": serializer.data.get("token")
            },
            "message": "Account created successfully. Check your email."
        }
        return Response(message, status=status.HTTP_201_CREATED)


class LoginAPI(GenericAPIView):
    """Login api view"""

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPI(RetrieveUpdateAPIView):
    """
    Retrieve and update users
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Get the currently login user
        """
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        update users
        """
        serializer_data = request.data

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
