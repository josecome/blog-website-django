from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.db.models import Q, Count
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
    PostByLinkSerializer,
    LikeSerializer,
    CommentSerializer,
    ShareSerializer,
)

class UserViewData(viewsets.ModelViewSet):
#    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    # permission_classes = [permissions.IsAuthenticated]


# Multiple Posts
class getMultiplePostData(viewsets.ModelViewSet):
#    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all().annotate(
        count_likes=Count("tags", filter=Q(tags__tag='like')),
        count_loves=Count("tags", filter=Q(tags__tag='love')),
        count_sads=Count("tags", filter=Q(tags__tag='sad')),
        count_comments=Count("comments"),
        count_shares=Count("shares"),
        )[:2]


# Multiple Posts of specific user
class getPostDataByUser(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().annotate(
        count_likes=Count("tags", filter=Q(tags__tag='like')),
        count_loves=Count("tags", filter=Q(tags__tag='love')),
        count_sads=Count("tags", filter=Q(tags__tag='sad')),
        count_comments=Count("comments"),
        count_shares=Count("shares"),
        )[:4]
    
    def get_queryset(self):
        username = self.kwargs['username']
        if username:
            self.queryset = Post.objects.filter(user__username=username).annotate(
                count_likes=Count("tags", filter=Q(tags__tag='like')),
                count_loves=Count("tags", filter=Q(tags__tag='love')),
                count_sads=Count("tags", filter=Q(tags__tag='sad')),
                count_comments=Count("comments"),
                count_shares=Count("shares"),
            )
            return self.queryset
        else:
            return self.queryset


# Data for Specific Post
class getPostDataByLink(viewsets.ModelViewSet):
    serializer_class = PostByLinkSerializer
    queryset = Post.objects.all().annotate(
        count_likes=Count("tags", filter=Q(tags__tag='like')),
        count_loves=Count("tags", filter=Q(tags__tag='love')),
        count_sads=Count("tags", filter=Q(tags__tag='sad')),
        count_comments=Count("comments"),
        count_shares=Count("shares"),
        )[:4]
    
    def get_queryset(self):
        id = self.kwargs['id']
        if id:
            self.queryset = Post.objects.filter(id=id).annotate(
                count_likes=Count("tags", filter=Q(tags__tag='like')),
                count_loves=Count("tags", filter=Q(tags__tag='love')),
                count_sads=Count("tags", filter=Q(tags__tag='sad')),
                count_comments=Count("comments"),
                count_shares=Count("shares"),
            )
            return self.queryset
        else:
            return self.queryset


# Post Atributes for Multiple Posts
class getMultipleLikesData(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        p = self.request.query_params.getlist('t', '')
        likes = Like.objects.filter(post__in=list(p))
        return likes


class getMultipleCommentsData(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        p = self.request.query_params.getlist('t', '')
        comments = Like.objects.filter(post__in=list(p))
        return comments


class getMultipleSharesData(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        p = self.request.query_params.getlist('t', '')
        shares = Like.objects.filter(post__in=list(p))
        return shares


class getLikesData(generics.ListAPIView):
    serializer_class = LikeSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        likes = Like.objects.filter(post=pk)
        return likes


class getCommentsData(generics.ListAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        comments = Comment.objects.filter(post=pk)
        return comments


class getSharesData(generics.ListAPIView):
    serializer_class = LikeSerializer
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