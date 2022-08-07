from rest_framework.serializers import ModelSerializer
from posts import models as post_models

class CategorySerializer(ModelSerializer):

    class Meta:
        model = post_models.Category
        fields = ("pk", "name",)

class TagSerializer(ModelSerializer):

    class Meta:
        model = post_models.Tag
        fields = ("pk", "name",)

class PostSerializer(ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = post_models.Post
        fields = ("pk", "category", "tags", "author", "created_at", "updated_at", "liked_users", "viewed_users", "scrapped_users",)