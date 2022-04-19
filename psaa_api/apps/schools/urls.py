from django.urls import path

from .views import (CreateGetSchoolAPI)

app_name = 'schools'

urlpatterns = [
    path('schools/', CreateGetSchoolAPI.as_view(), name='schools')
]
