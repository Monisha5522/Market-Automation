import re
import logger
from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        if data['name'] == "":
            return False
        elif not re.match('[A-Za-z\s]', data['name']):
            logger.error("name should not contain numeric character")
            raise serializers.ValidationError('name should not contain numeric character')
        return data

        if data['name'] == "":
            return False
        elif not (URLValidator, data['url']):
            logger.error('enter a proper url')
            raise serializers.ValidationError('enter a proper url')
        return data

