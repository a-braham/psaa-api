from django.urls import path

from .views import (
    CreateGetSchoolAPI, CreateGetStudentAPI,
    DeleteStudentAPI, RetrieveIsiboAPI, RetrieveUpdateSchoolAPI)

app_name = 'schools'

urlpatterns = [
    path('schools/', CreateGetSchoolAPI.as_view(), name='schools'),
    path('schools/<id>', RetrieveUpdateSchoolAPI.as_view(), name='school'),
    path('isibo/<id>', RetrieveIsiboAPI.as_view(), name='isibo'),
    path('schools/<id>/students/',
         CreateGetStudentAPI.as_view(), name='students'),
    path('schools/<id>/students/<student_id>/',
         DeleteStudentAPI.as_view(), name='drop')
]
