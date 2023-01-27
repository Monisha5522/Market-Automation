import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from automation_exception import DataNotExist
from rest_framework.views import APIView
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
            credential = Credential.objects.filter(pk=pk, is_active=True)
            logger.info(f"looking for the user {pk}")
            if not credential:
                raise DataNotExist("NO_DATA")
            serializer = CredentialSerializer(credential, many=True)
            return Response(serializer.data)
        except DataNotExist:
            logger.error(f'no data found found for the credential')
            return HttpResponse({f"Data not found for the credential {pk}"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, **kwargs):
        """
         This method is to get credentials
         :param  request
         """
        credential = Credential.objects.filter(is_active=True)
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


class DeleteCredential(APIView):
    @staticmethod
    def delete(request, pk):
        """
        This method is to remove credential
        :param request:
        :param pk:
        :return: boolean
        """
        try:
            credential = Credential.objects.get(pk=pk)
            if credential.is_active:
                logger.info(f"looking for the user {pk}")
                credential.is_active = False
                credential.save()
                logger.info(f"credential deleted successfully {pk}")
                return Response({"credential deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Detail ": "Data not found for what your looking"}, status=status.HTTP_400_BAD_REQUEST)
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Data not found"}, status=status.HTTP_400_BAD_REQUEST)
