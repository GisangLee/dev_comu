from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from accounts import utils
from accounts import perms
from accounts.swagger import swagger_utils, swagger_ser
from comments import models as comment_models
from comments import serializer as comment_ser

# 댓글 생성
# 댓글 보기 ( Pagination )
# 댓글 수정
# 댓글 삭제
class Comment(APIView):

    @swagger_auto_schema(manual_parameters=swagger_utils.login_required, tags=["댓글 모둡 불러오기"])
    def get(self, request, page=1):

        page = int(page)

        page_size = 10

        limit = page_size * page
        offset = limit - page_size

        all_comments = list(comment_models.Comment.objects.select_related("author").prefetch_related("child_comments", "child_comments__author", "author__profile_images").all())

        all_comments = all_comments[offset : limit]

        all_comments_ser = comment_ser.CommentSerializer(all_comments, many = True)

        res = utils.api_response(
            action = "댓글 모두 불러오기",
            method = "GET",
            url = "/comments/",
            error ="",
            message = all_comments_ser.data,
            status = "success"
        )

        return Response(res, status = status.HTTP_200_OK)