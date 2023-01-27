from django.urls import path, include
from rest_framework.routers import DefaultRouter
from role.views import RoleViewSet, DeleteRole

router = DefaultRouter()
router.register('automation/role', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('automation/role/restore/<int:pk>', DeleteRole.as_view()),
    path('automation/role/<int:pk>', RoleViewSet.retrieve)
]
