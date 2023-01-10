from django.urls import path, include
from rest_framework.routers import DefaultRouter
from post.views import PostViewSet

router = DefaultRouter()
router.register('automation/post', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('automation/post/<int:pk>', PostViewSet.retrieve)
]
