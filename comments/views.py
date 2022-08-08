from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from accounts import utils
from accounts import perms
from accounts.swagger import swagger_utils
from posts import models as post_models
from comments import models as comment_models
from comments import serializer as comment_ser
from comments.swagger import swagger_ser as comment_swagger_ser

# 댓글 보기 ( Pagination )
# 댓글 생성
class Comments(APIView):
    permission_classes = [perms.AllowAny]

    # 댓글 보기 ( Pagination )
    @swagger_auto_schema(manual_parameters=swagger_utils.get_all_comments, tags=["댓글 모두 불러오기"])
    def get(self, request, page=1):

        page = int(request.GET.get("page", 1))

        page_size = 10

        limit = page_size * page
        offset = limit - page_size

        all_comments = list(comment_models.Comment.objects
            .select_related("author")
            .prefetch_related("author__profile_images", "child_comments", "child_comments__author",
            "child_comments__author__profile_images", "liked_users", "disliked_users",
            "child_comments__liked_users", "child_comments__disliked_users")
            .all()
        )

        all_comments = all_comments[offset : limit]

        all_comments_ser = comment_ser.CommentSerializer(all_comments, many = True)

        res = utils.api_response(
            action = "댓글 모두 불러오기",
            method = "GET",
            url = "/comments",
            error ="",
            message = all_comments_ser.data,
            status = "success"
        )

        return Response(res, status = status.HTTP_200_OK)

    # 댓글 생성
    @swagger_auto_schema(request_body=comment_swagger_ser.CreateComment, manual_parameters=swagger_utils.login_required, tags=["댓글 생성"])
    def post(self, request):
        
        post_id = request.data.get("post_id", None)
        desc = request.data.get("desc", None)

        logged_in_user = request.user

        if post_id is None:
            res = utils.api_response(
                action = "댓글 생성",
                method = "POST",
                url = "/comments",
                error ="댓글이 속할 게시글 ID가 필요합니다.",
                message = "",
                status = "fail"
            )

            return Response(res, status = status.HTTP_400_BAD_REQUEST)

        elif desc is None:
            res = utils.api_response(
                action = "댓글 생성",
                method = "POST",
                url = "/comments",
                error ="댓글 내용을 요청 정보에 넣어주세요.",
                message = "",
                status = "fail"
            )

            return Response(res, status = status.HTTP_400_BAD_REQUEST)

        try:
            post = post_models.Post.objects.get(pk = post_id)

            if post:
                new_comment = comment_models.Comment.objects.create(post = post, author = logged_in_user)
                new_comment.desc = desc
                new_comment.save()

                res = utils.api_response(
                    action = "댓글 생성",
                    method = "POST",
                    url = "/comments",
                    error ="",
                    message = "댓글이 생성되었습니다.",
                    status = "success"
                )

                return Response(res, status = status.HTTP_201_CREATED)


        except post_models.Post.DoesNotExist:
            res = utils.api_response(
                action = "댓글 생성",
                method = "POST",
                url = "/comments",
                error ="존재하지 않는 게시글에는 댓글을 달 수 없습니다.",
                message = "",
                status = "fail"
            )

            return Response(res, status = status.HTTP_400_BAD_REQUEST)




# 댓글 상세
# 댓글 수정
# 댓글 삭제
class Comment(APIView):

    # 댓글 상세
    @swagger_auto_schema(manual_parameters=swagger_utils.login_required, tags=["댓글 상세보기"])
    def get(self, request, comment_pk):
        
        try:
            comment = comment_models.Comment.objects\
                .select_related("author")\
                .prefetch_related("author__profile_images", "child_comments", "child_comments__author",
                "child_comments__author__profile_images", "liked_users", "disliked_users",
                "child_comments__liked_users", "child_comments__disliked_users")\
                .get(pk = comment_pk)

            if comment:
                
                comment_json = comment_ser.CommentSerializer(comment)

                res = utils.api_response(
                    action = "댓글 상세",
                    method = "GET",
                    url = "/comments/comment/<int:comment_pk>",
                    error = "",
                    message = comment_json.data,
                    status = "success"
                )

                return Response(res, status = status.HTTP_200_OK)

        except comment_models.Comment.DoesNotExist:
            
            res = utils.api_response(
                action = "댓글 상세",
                method = "GET",
                url = "/comments/comment/<int:comment_pk>",
                error ="존재하지 않는 댓글입니다.",
                message = "",
                status = "fail"
            )

            return Response(res, status = status.HTTP_400_BAD_REQUEST)