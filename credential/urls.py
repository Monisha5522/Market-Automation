from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CredentialViewSet, DeleteCredential

router = DefaultRouter()
router.register('automation/credential', CredentialViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('automation/credential/restore/<int:pk>', DeleteCredential.as_view()),
    path('automation/credential/<int:pk>', CredentialViewSet.retrieve)
]