from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "telephone", "email", "role", "is_active", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # ✅ hash password on creation
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # ✅ hash password on update

        instance.save()
        return instance



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class TakenPostSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.full_name", read_only=True)
    client_phone = serializers.CharField(source="client.telephone", read_only=True)
    post_name = serializers.CharField(source="post.full_name", read_only=True)
    religion = serializers.CharField(source="post.religion", read_only=True)
    gender = serializers.CharField(source="post.gender", read_only=True)
    photo = serializers.CharField(source="post.photo", read_only=True)
    has_exp = serializers.CharField(source="post.has_exp", read_only=True)

    class Meta:
        model = TakenPost
        fields = ["id", "client", "client_name", "client_phone", "post", "post_name", "religion", "has_exp", "gender",  "photo","taken_at"]
        read_only_fields = ["taken_at", "client", "client_name", "client_phone", "post_name",  "gender", "photo", "religion",]

    def create(self, validated_data):
        validated_data["client"] = self.context["request"].user
        return super().create(validated_data)


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = "__all__"
        read_only_fields = ["name", "uploaded_at"]  # auto-generated fields