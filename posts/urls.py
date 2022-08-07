from django.urls import path
from posts import views as post_views

app_name = "posts"

urlpatterns = [
    path("post", post_views.Post.as_view()),
    path("post/<int:post_pk>", post_views.PostSpecific.as_view()),
    path("category", post_views.Category.as_view()),
]
