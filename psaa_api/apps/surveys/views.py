from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from psaa_api.utils.paginator import (Paginator)
from .models import (Survey)
from .serializers import (SurveySerializer)

User = get_user_model()


class CreateGetSurveyAPI(ListCreateAPIView):
    """Create and get surveys"""

    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def create(self, request):
        """Create a survey"""
        survey = request.data
        user = request.user
        serializer = self.serializer_class(
            data=survey,
            remove_fields=['created_at', 'updated_at'],
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        survey = serializer.save(user=user)
        data = serializer.data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )

    def get(self, request):
        """Get surveys"""
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
        surveys = self.filter_queryset(self.get_queryset())
        paginator = Paginator()
        paginator.page_size = page_limit
        result = paginator.paginate_queryset(surveys, request)
        serializer = SurveySerializer(
            result, many=True,
            context={'request': request},
            remove_fields=['updated_at']
        )
        response = paginator.get_paginated_response({
            'surveys': serializer.data
        })
        if response.get('dataCount') == 0:
            response["message"] = "No data found"
        return Response(response)
