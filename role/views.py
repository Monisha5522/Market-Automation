from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from automation_exception import DataNotExist
from rest_framework.views import APIView
from .models import Role
from .serializers import RoleSerializer
from automation_logger import logger
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins


class RoleViewSet(ModelViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Role.objects.filter(is_active=True)
    serializer_class = RoleSerializer

    def create(self, request, **kwargs):
        """
        This method is used to create role
        :param request
        :return: response
        """
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("role created successfully")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, **kwargs):
        """
         This method is used to get particular role
         :param  request:
         :param pk:
         :return: response
         """
        try:
            kwargs.get(pk)
            role = Role.objects.filter(pk=pk, is_active=True)
            logger.info(f"looking for the role {pk}")
            if not role:
                raise DataNotExist("NO_DATA")
            serializer = RoleSerializer(role, many=True)
            return Response(serializer.data)
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({f'no data found found for the role {pk}'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, **kwargs):
        """
         This method is to get role
         :param  request
         """
        role = Role.objects.filter(is_active=True)
        serializer = RoleSerializer(role, many=True)
        return Response(serializer.data)


class DeleteRole(APIView):
    @staticmethod
    def delete(request, pk):
        """
        This method is to remove user
        :param request:
        :param pk:
        :return: boolean
        """
        try:
            role = Role.objects.get(pk=pk)
            if role.is_active:
                logger.info(f"looking for the user {pk}")
                role.is_active = False
                role.save()
                logger.info(f"role deleted successfully {pk}")
                return Response({"role deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Detail ": "Data not found for what your looking"}, status=status.HTTP_400_BAD_REQUEST)
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Data not found"}, status=status.HTTP_400_BAD_REQUEST)
