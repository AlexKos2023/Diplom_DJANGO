from rest_framework import serializers
from .models import Post, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'text', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'text', 'image', 'created_at', 'comments', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post']

    def create(self, validated_data):
        user = self.context['request'].user
        post_id = validated_data.get('post')
        existing_like = Like.objects.filter(post=post_id, user=user).exists()

        if existing_like:
            raise serializers.ValidationError("You have already liked this post.")

        return Like.objects.create(user=user, **validated_data)