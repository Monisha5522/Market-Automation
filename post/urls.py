from django.urls import path, include
from rest_framework.routers import DefaultRouter
from post.views import PostViewSet, DeletePost, AttachmentViewSet, DeleteAttachment

router = DefaultRouter()
router.register('automation/post', PostViewSet),
router.register('automation/attachment', AttachmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('automation/post/restore/<int:pk>', DeletePost.as_view()),
    path('automation/post/<int:pk>', PostViewSet.retrieve),
    path('automation/attachment/<int:pk>', AttachmentViewSet.retrieve),
    path('automation/attachment/restore/<int:pk>', DeleteAttachment.as_view()),
]
