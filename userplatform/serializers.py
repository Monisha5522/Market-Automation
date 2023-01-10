import re
import logger
from rest_framework import serializers
from userplatform.models import Platform


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'

    def validate(self, data):
        if data['name'] == "":
            return False
        elif not re.match('[A-Za-z\s]', data['name']):
            logger.error("name should not contain numeric character")
            raise serializers.ValidationError('name should not contain numeric character')
        return data
