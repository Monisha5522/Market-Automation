from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSets

router = DefaultRouter()
router.register('automation/user', UserViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('automation/user/<int:pk>', UserViewSets.retrieve)
]

