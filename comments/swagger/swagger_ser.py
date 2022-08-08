from rest_framework.serializers import Serializer, CharField, ListField

class CreateComment(Serializer):
    post_id = CharField()
    desc = CharField()

class CreateChildComment(Serializer):
    parent_comment_id = CharField()
    desc = CharField()


class ModifyCommentSerializer(Serializer):
    post_id = CharField()
    desc = CharField()

class ModifyChildCommentSerializer(Serializer):
    parent_comment_id = CharField()
    desc = CharField()