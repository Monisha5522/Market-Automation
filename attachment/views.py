import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins

from automation_exception import DataNotExist
from .models import Attachment
from .serializers import AttachmentSerializer
from automation_logger import logger


class AttachmentViewSet(ModelViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Attachment.objects.filter(is_active=True)
    serializer_class = AttachmentSerializer

    def create(self, request, **Kwargs):
        """
        This method is used to create attachment
        :param request
        :return: response
        """
        serializer = AttachmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, **Kwargs):
        """
         This method is used to get particular attachment
         :param  request:
         :param pk:
         :return: response
         """
        try:
            post_id = Kwargs.get(pk)
            attachment = Attachment.objects.get(pk=pk)
            logger.info(f"looking for the credential {post_id}")
            if attachment.is_active:
                serializer = AttachmentSerializer(attachment)
                return Response(serializer.data)
            return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, **Kwargs):
        """
         This method is to get attachment
         :param  request
         """
        attachment = Attachment.objects.all()
        serializer = AttachmentSerializer(attachment, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None, **Kwargs):
        """
        This method is to edit attachment detail
        :param request:
        :param pk:
        :return: response
        """
        try:
            attachment_id = Kwargs.get(pk)
            attachment = Attachment.objects.get(pk=pk)
            logger.info(f"looking for the post {attachment_id}")
            if attachment.is_active:
                serializer = AttachmentSerializer(attachment, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

# def post_picture(request, name, password):
#     name = Credential.name
#     password = Credential.password
#     bot = Bot()
#     bot.login(username=name, password=password)
#     bot.upload_photo("D:/python/pexels-pixabay-158063.jpg", caption="rose image")
