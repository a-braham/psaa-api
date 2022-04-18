from django.urls import path

from .views import (RegistrationAPI, LoginAPI, UserRetrieveUpdateAPI)

app_name = 'authentication'

urlpatterns = [
    path('auth/signup/', RegistrationAPI.as_view(), name='registration'),
    path('auth/login/', LoginAPI.as_view(), name='login'),
    path('users/', UserRetrieveUpdateAPI.as_view(), name='users')
]
