from django.db import models
from accounts import models as user_models

# 게시글 카테고리
class Category(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "category"

# 게시글
class Post(models.Model):
    author = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="posts")
    
    title = models.CharField(max_length=255, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)

    tags = models.ManyToManyField("Tag", related_name="posts", through="PostTag", blank=True, null=True)
    liked_users = models.ManyToManyField(user_models.User, related_name="post_liked_users", through="PostLikedUsers", blank=True, null=True)
    viewed_users = models.ManyToManyField(user_models.User, related_name="post_viewed_users", through="PostViewedUsers", blank=True, null=True) 
    scrapped_users = models.ManyToManyField(user_models.User, related_name="post_scrapped_users", through="PostScrappedUsers", blank=True, null=True) 

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "posts"

# 게시글 태그
class Tag(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "tags"

# 게시글 + 태그 M & N
class PostTag(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_tag_mn")
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="post_tag_mn")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "post_tags_set"


# 게시글 좋아요 M & N
class PostLikedUsers(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_liked_user_mn")
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="post_liked_user_mn")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "post_liked_user_set"

# 게시글 스크랩 M & N

class PostViewedUsers(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_viewed_mn")
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="post_viewed_mn")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "post_viewed_user_set"


# 게시글 조회 M & N
class PostScrappedUsers(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_scrapped_mn")
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="post_scrapped_mn")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "post_scrapped_user_set"
