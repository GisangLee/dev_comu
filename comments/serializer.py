from rest_framework.serializers import ModelSerializer
from accounts.serializers import UserSerializer, UserSerializerForLikedOrDisliked
from comments import models as comment_models

class CommentSerializer(ModelSerializer):
    author = UserSerializer()
    liked_users = UserSerializerForLikedOrDisliked(many = True)
    disliked_users = UserSerializerForLikedOrDisliked(many = True)

    class Meta:
        model = comment_models.ChildComment
        fields = ("pk", "author", "desc", "created_at", "update_at", "liked_users", "disliked_users",)

class CommentSerializer(ModelSerializer):
    author = UserSerializer()
    child_comments = CommentSerializer(many=True)
    liked_users = UserSerializerForLikedOrDisliked(many = True)
    disliked_users = UserSerializerForLikedOrDisliked(many = True)

    class Meta:
        model = comment_models.Comment
        fields = ("pk", "author", "created_at", "updated_at", "desc", "child_comments", "liked_users", "disliked_users",)