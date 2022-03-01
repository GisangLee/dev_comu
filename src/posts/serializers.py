from wsgiref.handlers import read_environ
from rest_framework import serializers
from . import models as post_models
from accounts import models as user_models


class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.UseProfile
        fields = ("file",)


class AuthorSerializer(serializers.ModelSerializer):
    profile = AuthorProfileSerializer(read_only=True)

    class Meta:
        model = user_models.User
        fields = (
            "pk",
            "username",
            "email",
            "is_admin",
            "profile",
        )


class PostPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = post_models.PostPhoto
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = post_models.Post
        fields = (
            "title",
            "desc",
            "author",
            "created_at",
            "like_user_set",
            "views_user_set",
        )


class PostListSerializer(serializers.ModelSerializer):
    photo = PostPhotoSerializer(read_only=True, many=True)

    class Meta:
        model = post_models.Post
        fields = (
            "pk",
            "author",
            "title",
            "desc",
            "like_user_set",
            "views_user_set",
            "category",
            "photo",
            "created_at",
        )


class PostCategorySerializer(serializers.ModelSerializer):
    posts = PostSerializer(read_only=True, many=True)

    class Meta:
        model = post_models.PostCategory
        fields = (
            "pk",
            "category",
            "posts",
        )
