from rest_framework import serializers

from psaa_api.utils.baseserializer import BaseSerializer
from .models import (IsiboUsers, School, Student)


class SchoolSerializer(BaseSerializer):
    """School serializer"""

    def __init__(self, *args, **kwargs):
        super(SchoolSerializer, self).__init__(*args, **kwargs)

    user = serializers.ReadOnlyField(source='admin')
    teacher = serializers.ReadOnlyField(source='get_teacher')
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
            'id', 'name', 'user', 'teacher', 'description', 'province', 'district',
            'enrollments', 'dropouts', 'status', 'students', 'activities',
            'created_at', 'updated_at'
        )

class IsiboSerializer(BaseSerializer):
    """isibo serializer"""
    def __init__(self, *args, **kwargs):
        super(IsiboSerializer, self).__init__(*args, **kwargs)

    students = serializers.ReadOnlyField()
    student = serializers.ReadOnlyField(source='get_student')
    isibo = serializers.ReadOnlyField(source='get_isibo')

    class Meta:
        model = IsiboUsers
        fields = (
            'id', 'students', 'student', 'isibo',
            'created_at', 'updated_at'
        )


class StudentSerializer(BaseSerializer):
    """Student serializer"""
    def __init__(self, *args, **kwargs):
        super(StudentSerializer, self).__init__(*args, **kwargs)

    user = serializers.ReadOnlyField(source='admin')
    # parent = serializers.ReadOnlyField(source='get_parent')
    school = serializers.ReadOnlyField(source='get_school')
    # isibo = serializers.ReadOnlyField(source='get_isibo')

    class Meta:
        model = Student
        fields = (
            'id', 'name', 'user', 'parent', 'email', 'school', 'isibo', 'birth_date',
            'level', 'phone_number', 'status', 'comment', 'gender',
            'created_at', 'updated_at'
        )
