from email import message
from webbrowser import get
from requests import Response
from ..schools.models import Isibo, School
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import (RegistrationSerializer,
                          LoginSerializer, AuthSerializer,
                          UsersSerializer, RolesSerializer)
from psaa_api.utils.authentication_handlers import AuthTokenHandler
from .renderers import UserJSONRenderer
from psaa_api.utils.paginator import (Paginator)
from .exceptions import (UserNotFound, RoleNotFound)
from .models import User, Role, Permission

User = get_user_model()


class RegistrationAPI(GenericAPIView):
    """Sign up api view"""

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        try:
            roles = Role.objects.filter(name__in=['volunteer'])
        except Exception as exc:
            raise RoleNotFound from exc
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=data.get("email"))
        for role in roles:
            Permission.objects.create(user=user, role=role)
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
        data = serializer.data

        def get_roles():
            """Get roles of the user"""
            permissions = Permission.objects.filter(user_id=serializer.data['id']).values()
            roles = []
            for permission in permissions:
                role = Role.objects.get(
                    pk=permission['role_id']
                )
                role = {
                    "id": role.id,
                    "name": role.name,
                }
                roles.append(role)
            return roles
        try:
            school = School.objects.get(user_id=serializer.data['id'])
            if school:
                data = serializer.data
                data['school'] = {
                    'id': school.id,
                    'name': school.name
                }
        except School.DoesNotExist:
            exit
        roles = get_roles()
        data['roles'] = roles
        return Response(data, status=status.HTTP_200_OK)


class AuthRetrieveUpdateAPI(RetrieveUpdateAPIView):
    """
    Retrieve and update current user
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = AuthSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Get the currently login user
        """
        serializer = self.serializer_class(request.user)

        try:
            school = School.objects.get(user=request.user)
            teacher = User.objects.get(id=school.teacher_id)
            data = serializer.data
            data['school'] = {
                'id': school.id,
                'name': school.name,
                'teacher': {
                    'id': teacher.id,
                    'username': teacher.username,
                    'email': teacher.email
                }
            }
            try:
                isibo = Isibo.objects.get(user_id=serializer.data['id'])
                data['isibo'] = {
                    'id': isibo.id,
                    'name': isibo.name,
                    'admin': serializer.data['username']
                }
                return Response(data, status=status.HTTP_200_OK)
            except Isibo.DoesNotExist:
                return Response(data, status=status.HTTP_200_OK)
        except School.DoesNotExist:
            data = serializer.data
            try:
                myClass = School.objects.get(teacher_id=serializer.data['id'])
                data['school'] = {
                    'id': myClass.id,
                    'name': myClass.name,
                    # 'isibo': {
                    #     'id': myClass.isibo.id,
                    #     'name': myClass.isibo.name
                    # }
                }
                return Response(data, status=status.HTTP_200_OK)

            except School.DoesNotExist:
                data = serializer.data
                data['school'] = {}
                return Response(data, status=status.HTTP_200_OK)

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


class UsersRetrieveUpdateAPI(ListAPIView):
    """
    Retrieve and update users
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsersSerializer
    queryset = User.objects.all()

    def get(self, request):
        """Get users"""
        page_limit = request.GET.get('page_limit')
        if not page_limit:
            page_limit = 100
        else:
            error_response = Response(
                data={
                    'details': 'Invalid page limit'
                },
                status=status.HTTP_404_NOT_FOUND,
            )
            if not page_limit.isdigit():
                return error_response
            elif int(page_limit) < 1:
                return error_response
        schools = self.filter_queryset(self.get_queryset())
        paginator = Paginator()
        paginator.page_size = page_limit
        result = paginator.paginate_queryset(schools, request)
        serializer = UsersSerializer(
            result, many=True,
            context={'request': request},
        )
        response = paginator.get_paginated_response({
            'users': serializer.data
        })
        if response.get('dataCount') == 0:
            response["message"] = "No data found"
        return Response(response)


class UserRetrieveUpdateAPI(RetrieveUpdateAPIView):
    """Retrieve a user and update other user"""

    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsersSerializer

    def retrieve_user(self, id):
        """Fetch one user"""
        try:
            user = User.objects.get(id=id)
            return user
        except User.DoesNotExist:
            raise UserNotFound

    def get(self, request, id):
        """Get one user"""
        user = self.retrieve_user(id)
        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        """Update user details"""
        user = self.retrieve_user(id)
        current_user = request.user
        if user and user != current_user:
            serializer = self.serializer_class(
                instance=user,
                data=request.data,
                partial=True,
                remove_fields=['created_at', 'updated_at'],
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            data = serializer.data
            return Response(
                data={'user': data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    "errors": {
                        "error": [
                            "Cannot edit this user!"
                        ]
                    }
                },
                status=status.HTTP_403_FORBIDDEN
            )


class GetRolesAPI(RetrieveUpdateAPIView):
    """
    Retrieve roles
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RolesSerializer

    def get(self, request):
        """
        Get user roles
        """
        roles = Permission.objects.filter(
            user=request.user)
        serializer = self.serializer_class(
            roles,
            many=True,
            context={"request": request}
        )

        return Response(
            data={"roles": serializer.data},
            status=status.HTTP_200_OK
        )
