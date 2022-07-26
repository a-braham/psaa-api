from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import School, Student
from .serializers import (SchoolSerializer, StudentSerializer)
from .exceptions import (SchoolNotFound, StudentDoesNotExist)
from psaa_api.utils.paginator import (Paginator)

User = get_user_model()


class CreateGetSchoolAPI(ListCreateAPIView):
    """Create and get schools"""

    permission_classes = [IsAuthenticated]
    serializer_class = SchoolSerializer
    queryset = School.objects.all()

    def create(self, request):
        """Create a school"""
        school = request.data
        user = school['user']
        user, created = User.objects.get_or_create(**user)
        user.set_password('12345')
        user.save()
        serializer = self.serializer_class(
            data=school,
            remove_fields=['created_at', 'updated_at'],
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        school = serializer.save(user=user)
        data = serializer.data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )

    def get(self, request):
        """Get schools"""
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
        serializer = SchoolSerializer(
            result, many=True,
            context={'request': request},
            remove_fields=['updated_at']
        )
        response = paginator.get_paginated_response({
            'schools': serializer.data
        })
        if response.get('dataCount') == 0:
            response["message"] = "No data found"
        return Response(response)


class CreateGetStudentAPI(ListCreateAPIView):
    """Create and get students"""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def create(self, request, **kwargs):
        """Create a student"""
        student = request.data
        try:
            id = kwargs['id']
            school_inst = RetrieveUpdateSchoolAPI()
            school = school_inst.retrieve_school(id)
            parent = User.objects.get(pk=student['parent'])
            request.POST._mutable = True
            user = request.user
            serializer = self.serializer_class(data=student)
            serializer.is_valid(raise_exception=True)
            student = serializer.save(
                user=user, parent=parent, school=school
            )
            serializer.save()
            school = school_inst.retrieve_school(id)
            serializer = SchoolSerializer(
                school,
                context={'school': id, 'request': request},
                many=False
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except School.DoesNotExist:
            raise SchoolNotFound

    def get(self, request, id):
        """Get students"""
        page_limit = request.GET.get('page_limit')
        if not page_limit:
            page_limit = 6
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
        school_inst = RetrieveUpdateSchoolAPI()
        school = school_inst.retrieve_school(id)
        students = Student.objects.filter(school=school, status='active')
        paginator = Paginator()
        paginator.page_size = page_limit
        result = paginator.paginate_queryset(students, request)
        serializer = StudentSerializer(
            result, many=True,
            context={'request': request},
            remove_fields=['updated_at']
        )
        response = paginator.get_paginated_response({
            'students': serializer.data
        })
        if response.get('dataCount') == 0:
            response["message"] = "No data found"
        return Response(response)


class RetrieveUpdateSchoolAPI(GenericAPIView):
    """Retrieve, update and delete a school"""
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolSerializer

    def retrieve_school(self, id):
        """Fetch one school"""
        try:
            school = School.objects.get(id=id)
            return school
        except School.DoesNotExist:
            raise SchoolNotFound

    def get(self, request, id):
        """Get one school"""
        school = self.retrieve_school(id)
        if school:
            serializer = SchoolSerializer(
                school,
                context={'school': id, 'request': request},
                many=False
            )
            return Response(
                {'school': serializer.data},
                status=status.HTTP_200_OK
            )

    def patch(self, request, id):
        """Update school details"""
        school = self.retrieve_school(id)
        user = request.user
        if school.user == user:
            serializer = SchoolSerializer(
                instance=school,
                data=request.data,
                partial=True,
                remove_fields=['created_at', 'updated_at'],
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            school = serializer.save()
            data = serializer.data
            return Response(
                data={'school': data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    "errors": {
                        "error": [
                            "Cannot edit a school that is not yours"
                        ]
                    }
                },
                status=status.HTTP_403_FORBIDDEN
            )

    def delete(self, request, id):
        """Delete a school"""
        school = self.retrieve_school(id)
        user = request.user
        if school.user == user:
            school.status = 'inactive'
            school.save()
            return Response(
                {'message': '{} has been disabled'.format(school.name)},
                status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    "errors": {
                        "error": [
                            "Cannot delete a school that is not yours"
                        ]}
                },
                status=status.HTTP_403_FORBIDDEN
            )


class DeleteStudentAPI(GenericAPIView):
    """Api for droping out students"""
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer

    def retrieve_student(self, id):
        """Fetch one student"""
        try:
            school = Student.objects.get(id=id)
            return school
        except School.DoesNotExist:
            raise SchoolNotFound

    def patch(self, request, id, student_id):
        """Drop a student"""
        try:
            data = request.data
            reason = data['reason']
            if not reason:
                return Response(
                    data={
                        "errors": {
                            "error": [
                                "Reason for dropping out must be provided"
                            ]}
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            school_inst = RetrieveUpdateSchoolAPI()
            school = school_inst.retrieve_school(id)
            student = self.retrieve_student(student_id)
            if student and student.status != 'inactive':
                student.status = 'inactive'
                student.comment = reason
                student.save()
                serializer = SchoolSerializer(
                    school,
                    context={'school': id, 'request': request},
                    many=False
                )
                return Response(
                    {
                        'students': serializer.data,
                        'message': 'Student dropped'
                    },
                    status.HTTP_200_OK
                )
            serializer = SchoolSerializer(
                    school,
                    context={'school': id, 'request': request},
                    many=False
                )   
            return Response(
                    {
                        'students': serializer.data,
                        'message': 'Student dropped'
                    },
                    status.HTTP_200_OK
                )
        except Student.DoesNotExist:
            raise StudentDoesNotExist
