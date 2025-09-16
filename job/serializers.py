from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "full_name", "telephone", "role"]

    def create(self, validated_data):
        # Use Django's create_user to hash password
        return User.objects.create_user(**validated_data)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

