from rest_framework.serializers import Serializer, CharField, ListField

class CreateCategorySerializer(Serializer):
    name = CharField()


class CreatePostSerializer(Serializer):
    category_id = CharField()
    title = CharField()
    desc = CharField()
    tags_id = ListField()
    tag_names = ListField()


class ModifyPostSerializer(Serializer):
    title = CharField()
    desc = CharField()
    tag_names = ListField()