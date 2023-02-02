from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSets, DeleteUser, MailSent, InstagramPost

router = DefaultRouter()
router.register('automation/user', UserViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('automation/user/restore/<int:pk>', DeleteUser.as_view()),
    path('automation/user/mail/<int:pk>/<int:user_id>', MailSent.as_view()),
    path('automation/user/mail/subject/', MailSent.as_view()),
    path('automation/user/instagram/picture/<int:user_id>/<int:pk>/<int:attachment_id>', InstagramPost.as_view())
]
