from rest_framework import serializers
from avatrade.social_network.models import User, Post, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'bio', 'role', 'location', 'company', 'created_at', 'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user_id', 'post_id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user_id', 'content', 'likes', 'created_at', 'updated_at']
