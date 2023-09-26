"""blog_website_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from blog import views
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from api import views as api_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('', views.Blogs, name="home"),    
    path('postlist/', views.PostList, name="postlist"),  
    
    path('posts/<str:username>', views.PageOfPostByUser, name="posts"),
    path('posts/post/<str:link>', views.getPostPage, name="post"),
    path('postdata/<str:link>', views.getPostDataByLink, name="postdata"),
    path('postscontent/<str:username>', views.PostbyUser, name="postscontent"),    
    path('postlikes/', views.PostLikes, name="postlikes"),
    path('postcomments/', views.PostComments, name="postcomments"),
    path('addremovelike/', views.addRemoveLike, name="addremovelike"),
    path('addcomment/', views.addComment, name="addcomment"),
    path('useratrib/', views.getUserAtrib, name="useratrib"),     
    path('login/', views.loginPage, name='login'),
    path('admin/', admin.site.urls),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registrationPage, name='register'),
    #path('content/<int:id>', views.Content, name="content"),
    path('content/<str:lnk>', views.Content, name="content"),
    path('change-password/', auth_views.PasswordChangeView.as_view()),
    path('contents/', include('contents.urls')),

    # API auth
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API (Getting Data)
    path('api/user_posts_list/', api_views.getMultiplePostData.as_view()),
    path('api/user_posts/<int:user>', api_views.getPostDataByUser.as_view()),
    path('api/posts/likes/', api_views.getMultipleLikesData.as_view()),
    path('api/posts/comments/', api_views.getMultipleCommentsData.as_view()),
    path('api/posts/shares/', api_views.getMultipleSharesData.as_view()),

    re_path(r'api/post/(?P<pk>[a-z0-9]+)$', api_views.getPostDataByLink.as_view()),
    path('api/post/<int:pk>/likes/', api_views.getLikesData.as_view()),
    path('api/post/<int:pk>/comments/', api_views.getCommentsData.as_view()),
    path('api/post/<int:pk>/shares/', api_views.getSharesData.as_view()),
]

router = DefaultRouter()
router.register(r'api/user', api_views.UserViewData, basename="user"),

urlpatterns += router.urls