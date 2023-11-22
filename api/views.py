from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.db.models import Count
# Create your views here.
from django.contrib.auth import get_user_model
from contents.models import (
    Post,
    Comment,
    Like,
    Share,
)
# from rest_framework import permissions

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserSerializer,
    PostSerializer,
    LikesSerializer,
    CommentsSerializer,
    SharesSerializer,
)

class UserViewData(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    # permission_classes = [permissions.IsAuthenticated]


# Multiple Posts of specific user
class getPostDataByUser(generics.ListAPIView):
    serializer_class = PostSerializer
    lookup_url_kwarg = "user"

    def get_queryset(self):        
        user = self.kwargs.get(self.lookup_url_kwarg)
        user_id = int(User.objects.get(username=user).pk)
        post = Post.objects.filter(user=user_id)
        return post


# Multiple Posts
class getMultiplePostData(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        post = Post.objects.all()
        return post


# Post Atributes for Multiple Posts
class getMultipleLikesData(generics.ListAPIView):
    serializer_class = LikesSerializer

    def get_queryset(self):
        p = self.request.query_params.getlist('t', '')
        likes = Like.objects.filter(post__in=list(p))
        return likes


class getMultipleCommentsData(generics.ListAPIView):
    serializer_class = LikesSerializer

    def get_queryset(self):
        p = self.request.query_params.getlist('t', '')
        comments = Like.objects.filter(post__in=list(p))
        return comments


class getMultipleSharesData(generics.ListAPIView):
    serializer_class = LikesSerializer

    def get_queryset(self):
        p = self.request.query_params.getlist('t', '')
        shares = Like.objects.filter(post__in=list(p))
        return shares


# Data for Specific Post
class getPostDataByLink(generics.ListAPIView):
    serializer_class = PostSerializer
    lookup_url_kwarg = "lnk"

    def get_queryset(self):
        lnk = self.kwargs.get(self.lookup_url_kwarg)
        post = Post.objects.filter(link=lnk)
        return post


class getLikesData(generics.ListAPIView):
    serializer_class = LikesSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        likes = Like.objects.filter(post=pk)
        return likes


class getCommentsData(generics.ListAPIView):
    serializer_class = CommentsSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        comments = Comment.objects.filter(post=pk)
        return comments


class getSharesData(generics.ListAPIView):
    serializer_class = LikesSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        shares = Like.objects.filter(post=pk)
        return shares
    
class CountPostLikes(View):

    def get(self, request):
        data = Like.objects.all().values('post_id').annotate(total=Count('post_id')).order_by('total')
        array_data = ''
        for d in data:
            array_data += str(d['post_id']) + ":" + str(d['total']) + ";"
        
        return HttpResponse(array_data)


class CountPostComments(View):

    def get(self, request):
        data = Comment.objects.all().values('post_id').annotate(total=Count('post_id')).order_by('total')
        array_data = ''
        for d in data:
            array_data += str(d['post_id']) + ":" + str(d['total']) + ";"
        
        return HttpResponse(array_data)


class CountPostShares(View):

    def get(self, request):
        data = Share.objects.all().values('post_id').annotate(total=Count('post_id')).order_by('total')
        array_data = ''
        for d in data:
            array_data += str(d['post_id']) + ":" + str(d['total']) + ";"
        
        return HttpResponse(array_data)


class UserAtributes(View):

    def get(self, request):
        array_data = ''
        aa = request.GET['ids']
        print(aa)
        ArrayOfIds = request.GET['ids'].split(',')
        data = User.objects.filter(pk__in=ArrayOfIds)
        for d in data:
            array_data += str(d.pk) + ":" + str(d.username) + ";"
      
        return HttpResponse(array_data)    