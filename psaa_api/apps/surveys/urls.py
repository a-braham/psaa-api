from django.urls import path

from .views import (CreateGetSurveyAPI, StatisticsAPI)

app_name = 'surveys'

urlpatterns = [
    path('surveys/', CreateGetSurveyAPI.as_view(), name='surveys'),
    path('statistics/', StatisticsAPI.as_view(), name='statistics'),
]
