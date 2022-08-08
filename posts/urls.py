from django.urls import path
from posts import views as post_views

app_name = "posts"

urlpatterns = [
    path("", post_views.Posts.as_view()),
    path("post/<int:post_pk>", post_views.Post.as_view()),
    path("category", post_views.Category.as_view()),
]
