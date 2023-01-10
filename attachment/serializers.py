import logger
from rest_framework import serializers
from attachment.models import Attachment
from django.core.validators import URLValidator


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

    def validate(self, data):
        if not (URLValidator, data['url']):
            logger.error('enter a proper url')
            raise serializers.ValidationError('enter a proper url')
        return data
