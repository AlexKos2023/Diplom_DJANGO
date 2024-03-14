from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Like
from rest_framework.response import Response
from rest_framework import status
from social_network.permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, CommentSerializer, LikeSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = serializer.instance
        if post.author != self.request.user:
            raise PermissionDenied("You do not have permission to update this post.")
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        user_id = self.request.user.id

        existing_like = Like.objects.filter(post=post_id, user=user_id).exists()
        if existing_like:
            return

        post = Post.objects.get(id=post_id)
        serializer.save(user=self.request.user, post=post)