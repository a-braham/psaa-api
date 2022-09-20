from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from psaa_api.apps.schools.models import School, Student
from psaa_api.apps.authentication.backends import Permissions

from psaa_api.utils.paginator import Paginator
from .models import Survey
from psaa_api.apps.activities.models import Activity
from .serializers import SurveySerializer

from django.db.models import Count, Q
from django.db import models
from django.db.models import Func

User = get_user_model()


class CreateGetSurveyAPI(ListCreateAPIView):
    """Create and get surveys"""

    # permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def create(self, request):
        """Create a survey"""
        survey = request.data
        user = request.user
        serializer = self.serializer_class(
            data=survey,
            remove_fields=["created_at", "updated_at"],
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        survey = serializer.save(user=user)
        data = serializer.data

        return Response(data=data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """Get surveys"""
        page_limit = request.GET.get("page_limit")
        if not page_limit:
            page_limit = 50
        else:
            error_response = Response(
                data={"details": "Invalid page limit"},
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
            result,
            many=True,
            context={"request": request},
            remove_fields=["updated_at"],
        )
        # response = paginator.get_paginated_response({"surveys": serializer.data})
        # if response.get("dataCount") == 0:
        #     response["message"] = "No data found"
        # return Response(response)
        data = serializer.data

        return Response(data=data, status=status.HTTP_200_OK)


class StatisticsAPI(ListAPIView):
    """ Get API statistics"""

    permission_classes = (
        IsAuthenticated,
        Permissions(['super_admin', 'school_admin'])
    )
    queryset = Survey.objects.all()

    def get(self, request):
        """Get statistics"""
        # Permissions(['admin']).has_permission(request)
        enrollments_vs_dropouts = (
            Activity.objects.filter(create_at__year="2022")
            .annotate(month=Month("create_at"))
            .values("month")
            .annotate(
                total=Count("id"),
                enrollments=Count("id", filter=Q(type="Enrollment")),
                dropouts=Count("id", filter=Q(type="Drop out")),
            )
            .order_by("month")
        )
        drop_out_by_gender = (
            Student.objects.values("gender")
            .order_by("gender")
            .annotate(count=Count("gender"))
        )
        drop_out_by_causes = (
            Student.objects.filter(status='inactive')
            .values("comment")
            .order_by("comment")
            .annotate(count=Count("comment"))
        )
        schools = (
            Student.objects.filter(status='inactive').values("school")
            .order_by("school")
            .annotate(count=Count("school"))
        )

        data = []
        for school in schools:
            school_obj = School.objects.get(pk=school["school"])
            school["school"] = {
                "id": school_obj.id,
                "name": school_obj.name,
                "province": school_obj.province,
                "district": school_obj.district,
            }
            data.append(school)
        # schools_inaccessibility_rate_by_districts =
        surveys = Survey.objects.count()
        users = User.objects.count()
        schools = School.objects.count()
        return Response(
            {
                "statistics": {
                    "surveys": surveys,
                    "users": users,
                    "schools": schools,
                    "enrollments_vs_dropouts": enrollments_vs_dropouts,
                    "drop_out_by_gender": drop_out_by_gender,
                    "drop_out_by_causes": drop_out_by_causes,
                    "drop_out_by_school": data,
                }
            },
            status=status.HTTP_200_OK,
        )


class Month(Func):
    function = "to_char"
    template = "TRIM(%(function)s(%(expressions)s, 'Month'))"
    output_field = models.CharField()
