import json
import constants

from django.http import HttpResponse
from instabot import Bot
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from sendgrid import SendGridAPIClient, Mail
from .serializers import UserSerializer
from automation_exception import DataNotExist
from automation_logger import logger
from post.models import Post
from user.models import User
from post.models import Attachment
from credential.models import Credential
from post.serializers import PostSerializer
from credential.serializers import CredentialSerializer
from post.serializers import AttachmentSerializer


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
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=instance, updated_by=instance)
        logger.info("user created successfully")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, **kwargs):
        """
         This method is to get users
         :param  request
         """
        users = User.objects.filter(is_active=True)
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
            user = User.objects.filter(pk=pk, is_active=True)
            logger.info(f"looking for the user {pk}")
            if not user:
                raise DataNotExist("NO_DATA")
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data)
        except DataNotExist:
            logger.error(f'no data found found for the {pk}')
            return HttpResponse({f"Data not found for the user {pk}"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        """
        This method is to edit user detail
        :param request:
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

        except KeyError:
            logger.error(f"invalid key")
            return Response({"you have entered invalid key"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValueError:
            logger.error(f"invalid value")
            return Response(f"invalid value", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                user.is_active = False
                user.save()
                logger.info(f"user deleted successfully {pk}")
                return Response({"user deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Detail ": "Data not found for what your looking"}, status=status.HTTP_400_BAD_REQUEST)
        except DataNotExist:
            logger.error(f'no data found found for the user {pk}')
            return HttpResponse({"Data not found"}, status=status.HTTP_400_BAD_REQUEST)


def get_email():
    return User.objects.values('email')


def get_post(pk):
    """
    This method is to get a particular post
    :param pk:
    """
    post = Post.objects.get(id=pk, status=False)
    post_serializer = PostSerializer(post, data=post.__dict__)
    post_serializer.is_valid(raise_exception=True)
    return post_serializer.data


def get_mail_by_id(user_id):
    user = User.objects.get(id=user_id, is_active=True)
    user_serializer = UserSerializer(user, data=user.__dict__)
    user_serializer.is_valid(raise_exception=True)
    return user_serializer.data


class MailSent(APIView):

    @staticmethod
    def get(request, **kwargs):
        """
         This method is to get users
         :param request:
         """
        return Response(get_email())

    @staticmethod
    def post(request, pk, user_id, *args, **kwargs):
        """
        This method is to send a mail to external user
        :param request:
        :param pk:
        """
        constant = constants.send_grid_key
        sg = SendGridAPIClient(api_key=constant)
        get_mail = get_mail_by_id(user_id)
        post = get_post(pk)
        subject = post['subject']
        content_file = open("C:/Users/Lenovo/marketautomation/automation/user/mail.txt").read()
        content = content_file.format(content=post['caption'])
        message = Mail(
            from_email=(constants.sender_mail, 'Hello'),
            to_emails=get_mail['email'],
            subject=subject,
            html_content=content
        )
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return HttpResponse({"Mail sent successfully"}, response.status_code)


def get_user_name(pk):
    """
    This method is to get particular values'
    :param: pk:
    """
    credential = Credential.objects.get(id=pk)
    credential_serializer = CredentialSerializer(credential, data=credential.__dict__)
    credential_serializer.is_valid(raise_exception=True)
    return credential_serializer.data


def get_attachment(pk):
    """
    This method is to get attachment detail of the particular user
    :param pk:
    """
    attachment = Attachment.objects.get(id=pk)
    attachment_serializer = AttachmentSerializer(attachment, data=attachment.__dict__)
    attachment_serializer.is_valid(raise_exception=True)
    return attachment_serializer


class InstagramPost(APIView):
    @staticmethod
    def post(request, pk, *args, **kwargs):
        """
        This method is to send a post in
        :param request:
        :param pk:
        """
        user_name = get_user_name(pk)
        caption = get_post(pk)
        url = get_attachment(pk)
        bot = Bot()
        bot.login(username=user_name['name'], password=user_name['password'], is_threaded=True)
        bot.upload_photo(url['url'], caption=caption['caption'])
        return HttpResponse("posted")
