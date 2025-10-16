from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'email', 'role']

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'full_name', 'religion']

    @action(detail=True, methods=["post"], url_path="take")
    def take_post(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.is_taken:
            return Response({"detail": "This post is already taken."}, status=status.HTTP_400_BAD_REQUEST)

        taken_serializer = TakenPostSerializer(data={"post": post.id, "client": user.id}, context={"request": request})
        taken_serializer.is_valid(raise_exception=True)
        taken_serializer.save()

        return Response({"detail": "Post successfully taken!", "post": PostSerializer(post).data})


class TakenPostViewSet(viewsets.ModelViewSet):
    queryset = TakenPost.objects.all().order_by('-taken_at')
    serializer_class = TakenPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'client']

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.CUSTOMER:
            return TakenPost.objects.filter(client=user)
        return TakenPost.objects.all()


class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Archive.objects.all().order_by('-uploaded_at')
    serializer_class = ArchiveSerializer
    permission_classes = [permissions.IsAuthenticated]