from django.urls import path
from . import views as post_views

app_name = "posts"

urlpatterns = [
    path("post", post_views.PostView.as_view()),
    path("post-list", post_views.PostListView.as_view()),
    path("cat", post_views.CatCreateView.as_view()),
]
