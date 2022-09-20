from rest_framework import serializers

from psaa_api.utils.baseserializer import BaseSerializer
from .models import (Survey)


class SurveySerializer(BaseSerializer):
    """Survey serializer"""

    def __init__(self, *args, **kwargs):
        super(SurveySerializer, self).__init__(*args, **kwargs)

    user = serializers.ReadOnlyField(source='admin')

    def get_survey_by_admin(self):
        request = self.context.get('request', None)

        if request.user.is_anonymous:
            return ((False, None))

        user = request.user.id
        survey = Survey.objects.get(id=user)

        return (user, survey)

    class Meta:
        model = Survey
        fields = (
            'id', 'type', 'user', 'name', 'reason', 'description', 'isibo', 'birth_date', 'gender', 'parent', 'phone_number', 'created_at', 'updated_at'
        )
