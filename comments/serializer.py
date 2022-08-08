from rest_framework.serializers import ModelSerializer
from accounts.serializers import UserSerializer, UserSerializerForMToN
from comments import models as comment_models

class ChildCommentSerializer(ModelSerializer):
    author = UserSerializer()
    liked_users = UserSerializerForMToN(many = True) 
    disliked_users = UserSerializerForMToN(many = True) 

    class Meta:
        model = comment_models.ChildComment
        fields = ("pk", "author", "desc", "created_at", "update_at", "liked_users", "disliked_users",)

class SimpleChildCommentSerializer(ModelSerializer):

    class Meta:
        model = comment_models.ChildComment
        fields = ("pk",)


class CommentSerializer(ModelSerializer):
    author = UserSerializer()
    child_comments = ChildCommentSerializer(many=True)
    liked_users = UserSerializerForMToN(many = True) 
    disliked_users = UserSerializerForMToN(many = True) 

    class Meta:
        model = comment_models.Comment
        fields = ("pk", "author", "created_at", "updated_at", "desc", "child_comments", "liked_users", "disliked_users",)

class SimpleCommentSerializer(ModelSerializer):
    child_comments = SimpleChildCommentSerializer(many=True)

    class Meta:
        model = comment_models.Comment
        fields = ("pk", "child_comments",)