from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from accounts import perms, utils
from accounts.swagger import swagger_utils, swagger_ser
from posts import models as post_models
from posts import serializer
from posts.swagger import swagger_ser as post_swagger_ser

# 카테고리 생성 ( 관리자 전용 )
class Category(APIView):
    permission_classes = [perms.AdminOnly]

    @swagger_auto_schema(request_body=post_swagger_ser.CreateCategorySerializer, manual_parameters=swagger_utils.login_required, tags=["카테고리 생성"])
    def post(self, request):

        category_name = request.data.get("name", None)

        if category_name is None:
            res = utils.api_response(action="카테고리 생성", method="GET", url="/posts/category", error="생성할 카테고리 이름을 지정해주세요.", message="", status="fail")

            return Response(res, status = status.HTTP_400_BAD_REQUEST)

        post_models.Category.objects.create(name=category_name)

        res = utils.api_response(action="카테고리 생성", method="GET", url="/posts/category", error="", message="카테고리가 생성되었습니다.", status="success")

        return Response(res, status = status.HTTP_201_CREATED)
        
# 게시글 상세
# 게시글 삭제
# 게시글 수정
class PostSpecific(APIView):

    # 게시글 상세
    @swagger_auto_schema(manual_parameters=swagger_utils.login_required, tags=["게시글 상세"])
    def get(self, request, post_pk):

        logged_in_user = request.user

        print(f"logged_in_user: {logged_in_user}")
        print(f"post pk : {post_pk}")

        try:
            post = post_models.Post.objects.select_related("author", "category").prefetch_related("tags", "liked_users", "viewed_users", "scrapped_users").get(pk=post_pk, is_deleted=False)

            if post:
                
                post_ser = serializer.PostSerializer(post)

                res = utils.api_response(action="게시글 상세", method="GET", url="/posts/post/<int:pk>", error="", message=post_ser.data, status="success")

                return Response(res, status = status.HTTP_200_OK)

        except post_models.Post.DoesNotExist:
                res = utils.api_response(action="게시글 상세", method="GET", url="/posts/post/<int:pk>", error="존재하지 않는 게시글입니다.", message="", status="fail")

                return Response(res, status = status.HTTP_400_BAD_REQUEST)

    # 게시글 수정
    @swagger_auto_schema(request_body=post_swagger_ser.ModifyPostSerializer, manual_parameters=swagger_utils.login_required, tags=["게시글 수정"])
    def patch(self, request, post_pk):

        logged_in_user = request.user

        try:
            post = post_models.Post.objects.select_related('author').get(pk = post_pk)

            if post:
                author = post.author

                print(f"logged_in_user: {logged_in_user}")
                print(f"post pk : {post_pk}")

                if logged_in_user != author:
                    res = utils.api_response(action="게시글 수정", method="PATCH", url="/posts/post", error="권한이 없습니다.", message="", status="fail")

                    return Response(res, status = status.HTTP_401_UNAUTHORIZED)

                
                title = request.data.get("title", post.title)
                desc = request.data.get("desc", post.desc)

                post.title = title
                post.desc = desc

                post.save()

                res = utils.api_response(action="게시글 수정", method="PATCH", url="/posts/post", error="", message="수정되었습니다.", status="success")

                return Response(res, status = status.HTTP_200_OK)

        except post_models.Post.DoesNotExist:
            res = utils.api_response(action="게시글 수정", method="PATCH", url="/posts/post", error="존재하지 않는 게시글입니다.", message="", status="fail")

            return Response(res, status = status.HTTP_400_BAD_REQUEST)




# 게시글 작성
class Post(APIView):

    @swagger_auto_schema(request_body=post_swagger_ser.CreatePostSerializer, manual_parameters=swagger_utils.login_required, tags=["게시글 작성"])
    def post(self, request):

        logged_in_user = request.user

        category_id = request.data.get("category_id", None)
        title = request.data.get("title", None)
        desc = request.data.get("desc", None)
        tags_id = request.data.get("tags_id", None)

        if category_id is None or title is None or desc is None:
            res = utils.api_response(action="게시글 작성", method="POST", url="/posts/post", error="카테고리, 제목 혹은 내용을 채워주세요.", message="", status="fail")

            return Response(res, status = status.HTTP_400_BAD_REQUEST)

        try:
            category = post_models.Category.objects.get(pk = category_id)

            if category:

                tags = list(post_models.Tag.objects.filter(pk__in = tags_id))

                new_post = post_models.Post.objects.create(author = logged_in_user, category = category)

                new_post.title = title
                new_post.desc = desc

                new_post.tags.add(*tags)
                new_post.save()

                res = utils.api_response(action="게시글 작성", method="POST", url="/posts/post", error="", message="게시글이 작성되었습니다.", status="success")

                return Response(res, status = status.HTTP_201_CREATED)

        except post_models.Category.DoesNotExist:
            res = utils.api_response(action="게시글 작성", method="POST", url="/posts/post", error="존재하지 않는 카테고리 입니다.", message="", status="fail")

            return Response(res, status = status.HTTP_400_BAD_REQUEST)



