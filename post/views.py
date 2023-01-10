import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins

from automation_exception import DataNotExist
from .models import Post
from .serializers import PostSerializer
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

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, **kwargs):
        """
         This method is used to get particular post
         :param  request:
         :param pk:
         :return: response
         """
        try:
            kwargs.get(pk)
            post = Post.objects.get(pk=pk)
            logger.info(f"looking for the post {pk}")
            if post.is_active:
                serializer = PostSerializer(post)
                return Response(serializer.data)
            return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, **kwargs):
        """
         This method is to get post
         :param  request
         """
        post = Post.objects.all()
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
