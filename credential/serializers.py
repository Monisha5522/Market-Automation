import logger
from rest_framework import serializers
from credential.models import Credential


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'

    def validate(self, data):
        if not ('^[A-Za-z][A-Za-z0-9_]{7,29}$', data['name']):
            logger.error('enter a proper url')
            raise serializers.ValidationError('enter a proper url')
        return data
