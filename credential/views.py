import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse
from automation_exception import DataNotExist
from .models import Credential
from .serializers import CredentialSerializer
from automation_logger import logger
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins


class CredentialViewSet(ModelViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Credential.objects.filter(is_active=True)
    serializer_class = CredentialSerializer

    def create(self, request, **kwargs):
        """
        This method is to create credential
        :param request
        :return:credential detail
        """
        serializer = CredentialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"successfully created credential")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
         This method is used to get particular credential
         :param  request:
         :param pk:
         :return: response
         """
        try:
            kwargs.get(pk)
            credential = Credential.objects.get(pk=pk)
            logger.info(f"looking for the user {pk}")
            if credential.is_active:
                serializer = CredentialSerializer(credential)
                return Response(serializer.data)
        except DataNotExist:
            logger.error(f'no data found found for the ')
            return JsonResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, **kwargs):
        """
         This method is to get credentials
         :param  request
         """
        credential = Credential.objects.all()
        serializer = CredentialSerializer(credential, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        """
        This method is to edit credential detail
        :param request:
        :param pk:
        :return: response
        """
        try:
            kwargs.get(pk)
            credential = Credential.objects.get(pk=pk)
            logger.info(f"looking for the user {pk}")
            if credential.is_active:
                serializer = CredentialSerializer(credential, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)


def delete_credential(request, pk):
    """
    This method is to remove credential
    :param request:
    :param pk:
    :return: boolean
    """
    try:
        credential = Credential.objects.get(pk=pk)
        logger.info(f"looking for the credential {pk}")
        if credential.is_active:
            serializer = CredentialSerializer(credential, data=request.data)
            serializer.data['is_active'] = True
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
    except DataNotExist:
        logger.error(f'no data found found for the {pk}')
        return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

