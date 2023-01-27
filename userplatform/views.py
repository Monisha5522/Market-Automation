import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from automation_exception import DataNotExist
from rest_framework.views import APIView
from .models import Platform
from .serializers import PlatformSerializer
from automation_logger import logger
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins


class PlatformViewSet(ModelViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Platform.objects.filter(is_active=True)
    serializer_class = PlatformSerializer

    def create(self, request, **kwargs):
        """
        This method is used to create platform
        :param request
        :return: response
        """
        serializer = PlatformSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"successfully created platform")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, **kwargs):
        """
         This method is used to get particular platform
         :param  request:
         :param pk:
         :return: response
         """
        try:
            kwargs.get(pk)
            platform = Platform.objects.filter(pk=pk, is_active=True)
            logger.info(f"looking for the platform {pk}")
            if not platform:
                raise DataNotExist("NO_DATA")
            serializer = PlatformSerializer(platform, many=True)
            return Response(serializer.data)
        except DataNotExist:
            logger.error(f'no data found found for the platform {pk}')
            return HttpResponse({f'no data found found for the platform {pk}'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, **kwargs):
        """
         This method is to get platform
         :param  request
         """
        platform = Platform.objects.filter(is_active=True)
        serializer = PlatformSerializer(platform, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        """
        This method is to edit platform detail
        :param request:
        :param pk:
        :return: response
        """
        try:
            kwargs.get(pk)
            platform = Platform.objects.get(pk=pk)
            logger.info(f"looking for the platform {pk}")
            if platform.is_active:
                serializer = PlatformSerializer(platform, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)


class DeletePlatform(APIView):
    @staticmethod
    def delete(request, pk):
        """
        This method is to remove platform
        :param request:
        :param pk:
        :return: boolean
        """
        try:
            platform = Platform.objects.get(pk=pk)
            if platform.is_active:
                logger.info(f"looking for the user {pk}")
                platform.is_active = False
                platform.save()
                logger.info(f"platform deleted successfully {pk}")
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"Detail ": "Data not found for what your looking"}, status=status.HTTP_400_BAD_REQUEST)
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Data not found"}, status=status.HTTP_400_BAD_REQUEST)

