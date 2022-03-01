from django.db.models import Prefetch
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models as post_models
from . import serializers as post_serializer


class CatCreateView(APIView):
    def post(self, request):
        serializer = post_serializer.PostCategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "OK"}, status=status.HTTP_201_CREATED)


class PostView(APIView):
    def post(self, request):
        logged_in_user = request.user
        serializer = post_serializer.PostSerializer(data=request.data)

        photos = request.FILES.get("photos")

        if serializer.is_valid():
            if photos:
                post = serializer.save(author=logged_in_user)
                for photo in photos:
                    post_photo = post_models.PostPhoto.objects.create(
                        post=post, file=photo
                    )
                    post_photo.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                post = serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, request):
        posts = post_models.PostCategory.objects.prefetch_related(
            Prefetch(
                "posts",
                queryset=post_models.Post.objects.prefetch_related(
                    "photos", "like_user_set", "views_user_set"
                ),
            )
        )
        serializer = post_serializer.PostCategorySerializer(posts, many=True)

        return Response(serializer.data)
