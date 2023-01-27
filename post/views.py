from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from automation_exception import DataNotExist
from .models import Post, Attachment
from .serializers import PostSerializer, AttachmentSerializer
from automation_logger import logger


class PostViewSet(ModelViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Post.objects.filter(is_active=True)
    serializer_class = PostSerializer

    def create(self, request, **Kwargs):
        """
        This method is used to create post
        :param request
        :return: response
        """
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        attachment_serializer = AttachmentSerializer(data=request.data['attachment'])
        attachment_serializer.is_valid(raise_exception=True)
        attachment_serializer.save()
        return Response(attachment_serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        """
         This method is used to get particular post
         :param  request:
         :param pk:
         :return: response
         """
        try:
            kwargs.get(pk)
            post = Post.objects.filter(pk=pk, is_active=True)
            logger.info(f"looking for the post {pk}")
            if not post:
                raise DataNotExist("no data found")
            serializer = PostSerializer(post, many=True)
            return Response(serializer.data)
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({f"Data not found for the post {pk}"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, **kwargs):
        """
         This method is to get post
         :param  request
         """
        post = Post.objects.filter(is_active=True)
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        """
        This method is to edit post detail
        :param request:
        :param pk:
        :return: response
        """
        try:
            kwargs.get(pk)
            post = Post.objects.get(pk=pk)
            logger.info(f"looking for the post {pk}")
            if post.is_active:
                serializer = PostSerializer(post, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)


class DeletePost(APIView):
    @staticmethod
    def delete(request, pk):
        """
        This method is to remove post
        :param request:
        :param pk:
        :return: boolean
        """
        try:
            post = Post.objects.get(pk=pk)
            if post.is_active:
                logger.info(f"looking for the user {pk}")
                post.is_active = False
                post.save()
                logger.info(f"post deleted successfully {pk}")
                return Response({"post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Detail ": "Data not found for what your looking"}, status=status.HTTP_400_BAD_REQUEST)
        except DataNotExist:
            logger.error(f'no data found for the {pk}')
            return HttpResponse({"Data not found"}, status=status.HTTP_400_BAD_REQUEST)


class AttachmentViewSet(ModelViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Attachment.objects.filter(is_active=True)
    serializer_class = AttachmentSerializer

    def retrieve(self, request, pk=None, **kwargs):
        """
         This method is used to get particular Attachment
         :param  request:
         :param pk:
         :return: response
         """
        try:
            kwargs.get(pk)
            attachment = Attachment.objects.filter(pk=pk, is_active=True)
            logger.info(f"looking for the post {pk}")
            if not attachment:
                raise DataNotExist("no data found")
            serializer = AttachmentSerializer(attachment, many=True)
            return Response(serializer.data)
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({f"Data not found for the post {pk}"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, **kwargs):
        """
         This method is to get post
         :param  request
         """
        attachment = Attachment.objects.filter(is_active=True)
        serializer = AttachmentSerializer(attachment, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        """
        This method is to edit post detail
        :param request:
        :param pk:
        :return: response
        """
        try:
            kwargs.get(pk)
            attachment = Attachment.objects.get(pk=pk)
            logger.info(f"looking for the post {pk}")
            if attachment.is_active:
                serializer = AttachmentSerializer(attachment, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)


class DeleteAttachment(APIView):
    @staticmethod
    def delete(request, pk):
        """
        This method is to remove post
        :param request:
        :param pk:
        :return: boolean
        """
        try:
            attachment = Attachment.objects.get(pk=pk)
            if attachment.is_active:
                logger.info(f"looking for the user {pk}")
                attachment.is_active = False
                attachment.save()
                logger.info(f"post deleted successfully {pk}")
                return Response({"post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Detail ": "Data not found for what your looking"}, status=status.HTTP_400_BAD_REQUEST)
        except DataNotExist:
            logger.error(f'no data found for the {pk}')
            return HttpResponse({"Data not found"}, status=status.HTTP_400_BAD_REQUEST)