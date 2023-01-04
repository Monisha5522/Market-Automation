from rest_framework import serializers
from automation.models import User, Credential, PlatformType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'


class PlatformTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformType
        fields = '__all__'
