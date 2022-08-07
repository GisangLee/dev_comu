from django.db import models
from accounts import models as user_models
from posts import models as post_models

class Comment(models.Model):
    author = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(post_models.Post, on_delete=models.CASCADE, related_name="comments")

    desc = models.TextField(blank=True, null=True)

    liked_users = models.ManyToManyField(user_models.User, related_name="comment_liked_users", through="CommentLikedUsers", blank=True, null=True)
    disliked_users = models.ManyToManyField(user_models.User, related_name="comment_disliked_users", through="CommentDisLikedUsers", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "comments"


class ChildComment(models.Model):
    author = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="child_comments")
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="child_comments")

    desc = models.TextField(blank=True, null=True)

    liked_users = models.ManyToManyField(user_models.User, related_name="child_comment_liked_users", through="ChildCommentLikedUsers", blank=True, null=True)
    disliked_users = models.ManyToManyField(user_models.User, related_name="child_comment_disliked_users", through="ChildCommentDisLikedUsers", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "child_comments"


# 댓글 좋아요 M & N
class CommentLikedUsers(models.Model):
    user = models.ForeignKey(user_models.User, related_name="comment_liked_user_mn", on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", related_name="comment_liked_user_mn", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "comment_liked_user_set"

# 댓글 싫어요 M & N
class CommentDisLikedUsers(models.Model):
    user = models.ForeignKey(user_models.User, related_name="comment_disliked_user_mn", on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", related_name="comment_disliked_user_mn", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "comment_disliked_user_set"




# 대댓글 좋아요 M & N
class ChildCommentLikedUsers(models.Model):
    user = models.ForeignKey(user_models.User, related_name="child_comment_liked_user_mn", on_delete=models.CASCADE)
    child_comment = models.ForeignKey("ChildComment", related_name="child_comment_liked_user_mn", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = "child_comment_liked_user_set"

# 대댓글 싫어요 M & N
class ChildCommentDisLikedUsers(models.Model):
    user = models.ForeignKey(user_models.User, related_name="child_comment_disliked_user_mn", on_delete=models.CASCADE)
    child_comment = models.ForeignKey("ChildComment", related_name="child_comment_disliked_user_mn", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "child_comment_disliked_user_set"