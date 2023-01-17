from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSets, DeleteUser, MailSent

router = DefaultRouter()
router.register('automation/user', UserViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('automation/user/<int:pk>', DeleteUser.as_view()),
    path('automation/user/mail', MailSent.as_view())
]
