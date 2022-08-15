from rest_framework import serializers

from psaa_api.utils.baseserializer import BaseSerializer
from .models import (School, Student)


class SchoolSerializer(BaseSerializer):
    """School serializer"""

    def __init__(self, *args, **kwargs):
        super(SchoolSerializer, self).__init__(*args, **kwargs)

    user = serializers.ReadOnlyField(source='admin')
    students = serializers.ReadOnlyField()
    activities = serializers.ReadOnlyField()

    def get_school_by_admin(self):
        request = self.context.get('request', None)

        if request.user.is_anonymous:
            return ((False, None))

        user = request.user.id
        school = School.objects.get(id=user)

        return (user, school)

    class Meta:
        model = School
        fields = (
            'id', 'name', 'user', 'description', 'province', 'district',
            'enrollments', 'dropouts', 'status', 'students', 'activities',
            'created_at', 'updated_at'
        )


class StudentSerializer(BaseSerializer):
    """Student serializer"""
    def __init__(self, *args, **kwargs):
        super(StudentSerializer, self).__init__(*args, **kwargs)

    user = serializers.ReadOnlyField(source='admin')
    # parent = serializers.ReadOnlyField(source='get_parent')
    school = serializers.ReadOnlyField(source='get_school')

    class Meta:
        model = Student
        fields = (
            'id', 'name', 'user', 'parent', 'school', 'birth_date',
            'level', 'phone_number', 'status', 'comment',
            'created_at', 'updated_at'
        )
