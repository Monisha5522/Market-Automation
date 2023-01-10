import re
import logger
from rest_framework import serializers
from role.models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

    def validate(self, data):
        if not re.match('[A-Za-z\s]', data['name']):
            logger.error("name should not contain numeric character")
            raise serializers.ValidationError('name should not contain numeric character')
        return data
