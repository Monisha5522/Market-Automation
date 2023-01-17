import re
from automation_logger import logger
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

        if data['phone'] == "":
            return False
        elif not re.match('^(0/91)?[7-9][0-9]{9}$', str(data['phone'])):
            logger.error('number should contain 10 digit')
            raise serializers.ValidationError('Enter a proper number, it should contain 10 digit')
        return data
