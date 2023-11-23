from rest_framework import routers
from . import views as api_views
from django.urls import path, re_path

router = routers.SimpleRouter()
router.register(r'users', api_views.UserViewData, basename="user")
router.register(r'posts', api_views.getMultiplePostData, basename="post-list")
router.register('post/(?P<id>[^/.]+)', api_views.getPostDataByLink, basename="post-details")
router.register('user-posts/(?P<username>[^/.]+)', api_views.getPostDataByUser, basename="user-posts")

urlpatterns = router.urls