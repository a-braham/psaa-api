from rest_framework import serializers

from psaa_api.utils.baseserializer import BaseSerializer
from .models import (School)


class SchoolSerializer(BaseSerializer):
    """School serializer"""

    def __init__(self, *args, **kwargs):
        super(SchoolSerializer, self).__init__(*args, **kwargs)

    user = serializers.ReadOnlyField(source='admin')

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
            'name', 'user', 'description', 'province', 'district',
            'enrollments', 'dropouts', 'status', 'created_at', 'updated_at'
        )
