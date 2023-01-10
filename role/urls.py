from django.urls import path, include
from rest_framework.routers import DefaultRouter
from role.views import RoleViewSet

router = DefaultRouter()
router.register('automation/role', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('automation/role/<int:pk>', RoleViewSet.retrieve)
]
