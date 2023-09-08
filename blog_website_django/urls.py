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
from django.urls import path
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
    path('api/postlist/', views.PostList, name="apipostlist"),  
    path('posts/<str:username>', views.PageOfPostByUser, name="posts"),
    path('posts/post/<str:link>', views.getPostPage, name="post"),
    path('postdata/<str:link>', views.getPostDataByLink, name="postdata"),
    path('api/postdata/<str:link>', views.getPostDataByLink, name="postdata"),
    path('postscontent/<str:username>', views.PostbyUser, name="postscontent"),
    path('api/postscontent/<str:username>', views.PostbyUser, name="postscontent"),
    path('postlikes/', views.PostLikes, name="postlikes"),
    path('postcomments/', views.PostComments, name="postcomments"),
    path('api/postlikes/', views.PostLikes, name="apipostlikes"),    
    path('api/postcomments/', views.PostComments, name="apipostcomments"),
    path('addremovelike/', views.addRemoveLike, name="addremovelike"),
    path('addcomment/', views.addComment, name="addcomment"),
    path('useratrib/', views.getUserAtrib, name="useratrib"),
    path('api/useratrib/', views.getUserAtrib, name="apiuseratrib"),    
    path('login/', views.loginPage, name='login'),
    path('admin/', admin.site.urls),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registrationPage, name='register'),
    #path('content/<int:id>', views.Content, name="content"),
    path('content/<str:lnk>', views.Content, name="content"),
    path('change-password/', auth_views.PasswordChangeView.as_view()),
    path('contents/', include('contents.urls')),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = DefaultRouter()
router.register(r'api/user', api_views.UserViewData, basename="user")
urlpatterns += router.urls