import json
import utils

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from sendgrid import SendGridAPIClient, Mail
from .serializers import UserSerializer
from automation_exception import DataNotExist
from automation_logger import logger
from post.models import Post
from user.models import User
from post.serializers import PostSerializer


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
        logger.info(f'user details')
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


class DeleteUser(APIView):
    @staticmethod
    def delete(request, pk):
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
                user.save()
                logger.info(f"user deleted successfully {pk}")
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"Detail ": "Data not found for what your looking"}, status=status.HTTP_400_BAD_REQUEST)
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({"Detail : ": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)


def get_email():
    return User.objects.values('email')


def get_post(pk):
    post = Post.objects.get(id=pk, status=False)
    print(post)
    post_serializer = PostSerializer(post, data=post.__dict__)
    print('2', post_serializer)
    post_serializer.is_valid(raise_exception=True)
    print(post_serializer)
    return post_serializer.data


class MailSent(APIView):

    @staticmethod
    def get(request, **kwargs):
        """
         This method is to get users
         :param  request
         """
        return Response(get_email())

    @staticmethod
    def post(request, pk, *args, **kwargs):
        constant = utils.send_grid_key
        sg = SendGridAPIClient(api_key=constant)
        print(sg)
        post = get_post(pk)
        print(post)
        subject = post['subject']
        print(subject)
        content_file = open("C:/Users/Lenovo/marketautomation/automation/user/mail.txt").read()
        content = content_file.format(content=post['caption'])
        message = Mail(
            from_email=('manishadarling52@gmail.com', 'Hello'),
            to_emails='monishasivanathan@gmail.com',
            # to_emails=To(get_email()),
            subject=subject,
            html_content=content
        )
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return HttpResponse({"Mail sent successfully"}, response.status_code)
