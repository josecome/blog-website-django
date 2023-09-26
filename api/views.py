from django.shortcuts import render
from rest_framework import generics

# Create your views here.
from django.contrib.auth import get_user_model
from contents.models import (
    Posts as Post, 
    Likes as Like, 
    Comments as Comment, 
    Shares as Share
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


class getPostDataByLink(generics.ListAPIView):
    serializer_class = PostSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        post = Post.objects.filter(id=pk)
        return post


class getLikesData(generics.ListAPIView):
    serializer_class = LikesSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        likes = Like.objects.filter(post=pk)
        return likes


class getCommentsData(generics.ListAPIView):
    serializer_class = LikesSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        comments = Like.objects.filter(post=pk)
        return comments


class getSharesData(generics.ListAPIView):
    serializer_class = LikesSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        shares = Like.objects.filter(post=pk)
        return shares