import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_protect

from .automation_exception import DataNotExist
from .models import User, Credential, PlatformType
from .serializers import UserSerializer, CredentialSerializer, PlatformTypeSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins


class UserViewSets(ModelViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = User.objects.filter(is_active=False)
    serializer_class = UserSerializer


class CredentialViewSet(ModelViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Credential.objects.filter(is_active=False)
    serializer_class = CredentialSerializer


class PlatformTypeViewSet(ModelViewSet, mixins.DestroyModelMixin, mixins.DestroyModelMixin):
    queryset = PlatformType.objects.filter(is_active=False)
    serializer_class = PlatformTypeSerializer


@csrf_protect
def create_user(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@csrf_protect
def get_user(request, user_id):
    try:
        user = User.objects.get(user=user_id)
        if user.is_active:
            return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
    except DataNotExist:
        return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)


@csrf_protect
def edit_user(request, user_id):
    try:
        user = User.objects.get(user=user_id)
        if user.is_active:
            return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
    except DataNotExist:
        return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_protect
def remove_user(request, user_id):
    try:
        user = User.objects.get(user=user_id)
        if user.is_active:
            return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
    except DataNotExist:
        return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        serializer = UserSerializer(user, data=request.data)
        serializer.data['is_active'] = True
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_protect
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@csrf_protect
def create_credential(request):
    serializer = CredentialSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@csrf_protect
def get_credential(request):
    credential = Credential.objects.all()
    serializer = CredentialSerializer(credential, many=True)
    return Response(serializer.data)


@csrf_protect
def get_credential(request, credential_id):
    try:
        user = User.objects.get(user=credential_id)
        if user.is_active:
            return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
    except DataNotExist:
        return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = CredentialSerializer(user)
        return Response(serializer.data)


@csrf_protect
def edit_credential(request, credential_id):
    try:
        credential = Credential.objects.get(user=credential_id)
        if credential.is_active:
            return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
    except DataNotExist:
        return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        serializer = UserSerializer(credential, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_protect
def remove_user(request, user_id):
    try:
        credential = Credential.objects.get(user=user_id)
        if credential.is_active:
            return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
    except DataNotExist:
        return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        serializer = CredentialSerializer(credential, data=request.data)
        serializer.data['is_active'] = True
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
