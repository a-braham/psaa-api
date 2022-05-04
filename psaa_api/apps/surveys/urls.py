from django.urls import path

from .views import (CreateGetSurveyAPI)

app_name = 'surveys'

urlpatterns = [
    path('surveys/', CreateGetSurveyAPI.as_view(), name='surveys'),
]
