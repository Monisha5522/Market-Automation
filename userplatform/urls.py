from django.urls import path, include
from rest_framework.routers import DefaultRouter
from userplatform.views import PlatformViewSet

router = DefaultRouter()
router.register('automation/platform', PlatformViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('automation/platform/<int:pk>', PlatformViewSet.retrieve)
]
