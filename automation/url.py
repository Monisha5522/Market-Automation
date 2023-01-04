from django.urls import path, include
from rest_framework.routers import DefaultRouter
from automation.views import UserViewSets, CredentialViewSet

router = DefaultRouter()
router.register('user/view', UserViewSets)
router.register('credential', CredentialViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
