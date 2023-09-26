
from rest_framework import serializers
from django.contrib.auth import get_user_model
from contents.models import (
    Posts as Post, 
    Likes as Like, 
    Comments as Comment, 
    Shares as Share
)


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = get_user_model()
        fields = "__all__"


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "post_content", "post_type", "link", "user"]


class PostIdSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ["id"]


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["type_of_like", "post_liked_link", "user"]


class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment", "post_commented_link", "user"]


class SharesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Share
        fields = ["post_shared_link", "user"]
