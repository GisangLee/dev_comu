from django.db import models
from accounts import models as user_models


class PostCategory(models.Model):
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category

    class Meta:
        db_table = "post_category"


class Post(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    author = models.ForeignKey(
        user_models.User, related_name="posts", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like_user_set = models.ManyToManyField(
        user_models.User, blank=True, related_name="post_likes"
    )

    views_user_set = models.ManyToManyField(
        user_models.User, related_name="post_views", blank=True
    )

    category = models.ForeignKey(
        "PostCategory",
        related_name="posts",
        on_delete=models.CASCADE,
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "post"


class PostPhoto(models.Model):
    post = models.ForeignKey("Post", related_name="photos", on_delete=models.CASCADE)
    file = models.ImageField(upload_to="posts/%Y/%m/%d")

    def __str__(self):
        return self.post

    class Meta:
        db_table = "post_photo"
