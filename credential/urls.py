from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CredentialViewSet

router = DefaultRouter()
router.register('automation/credential', CredentialViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('automation/credential/<int:pk>', CredentialViewSet.retrieve)
]