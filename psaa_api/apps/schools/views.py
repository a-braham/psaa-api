from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import School
from .serializers import (SchoolSerializer)
from psaa_api.utils.paginator import (Paginator)

User = get_user_model()


class CreateGetSchoolAPI(ListCreateAPIView):
    """Create and get school"""

    permission_classes = (IsAuthenticatedOrReadOnly, )
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
        """Get Fschools"""
        page_limit = request.GET.get('page_limit')
        if not page_limit:
            page_limit = 1
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
