from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from .models import *
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]


class PostViewSet(viewsets.ModelViewSet):
      queryset=Post.objects.all()
      serializer_class=PostSerializer
      renderer_classes=[JSONRenderer]
      permission_classes=[IsAuthenticated]
