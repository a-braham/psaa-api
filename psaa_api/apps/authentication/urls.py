from django.urls import path

from .views import (
    GetRolesAPI, RegistrationAPI, LoginAPI,
    AuthRetrieveUpdateAPI, UsersRetrieveUpdateAPI,
    UserRetrieveUpdateAPI, GetRolesAPI
)

app_name = 'authentication'

urlpatterns = [
    path('auth/signup/', RegistrationAPI.as_view(), name='registration'),
    path('auth/login/', LoginAPI.as_view(), name='login'),
    path('auth/', AuthRetrieveUpdateAPI.as_view(), name='auth'),
    path('users/', UsersRetrieveUpdateAPI.as_view(), name='users'),
    path('users/<id>', UserRetrieveUpdateAPI.as_view(), name='user'),
    path('roles/', GetRolesAPI.as_view(), name='roles')
]
