
from rest_framework import serializers
from django.contrib.auth import get_user_model
from contents.models import (
    Posts as Post, 
    Likes as Like, 
    Comments as Comment, 
    Shares as Share
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = "__all__"


class getPostDataByLinkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = "__all__"


class PostbyUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = "__all__"


class PostLikesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = "__all__"


class PostCommentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = "__all__"


class getUserAtribSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = "__all__"

