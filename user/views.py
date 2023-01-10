import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse
from .models import User
from .serializers import UserSerializer
from automation_exception import DataNotExist
from automation_logger import logger
from rest_framework import viewsets
from rest_framework.decorators import api_view


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is to create user
        :param  request
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.created_by = instance
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("user created successfully")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, **kwargs):
        """
         This method is to get users
         :param  request
         """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        logger.info(f'*********user details******')
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
         This method is used to get particular person
         :param  request:
         :param pk:
         :return: response
         """
        try:
            kwargs.get(pk)
            user = User.objects.get(pk=pk)
            logger.info(f"looking for the user {pk}")
            if user.is_active:
                serializer = UserSerializer(user)
                return Response(serializer.data)
        except DataNotExist:
            print(1)
            logger.error(f'no data found found for the ')
            return JsonResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        """
        This method is to edit user detail
        :param request:
        :param pk:
        :return: response
        """
        try:
            kwargs.get(pk)
            user = User.objects.get(pk=pk)
            logger.info(f"looking for the user {pk}")
            if user.is_active:
                serializer = UserSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            return HttpResponse(json.dumps({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST))
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, pk):
    print(0)
    """
    This method is to remove user
    :param request:
    :param pk:
    :return: boolean
    """
    try:
        user = User.objects.get(pk=pk)
        if user.is_active:
            logger.info(f"looking for the user {pk}")
            user.is_active = True
            user.save()
            logger.info(f"user deleted successfully {pk}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"Detail ": "data not found"}, status=status.HTTP_400_BAD_REQUEST)
    except DataNotExist:
        logger.error(f'no data found found for the {pk}')
        return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

