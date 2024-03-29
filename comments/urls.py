from django.urls import path
from comments import views as comment_views

app_name = "comments"

urlpatterns = [
    path("", comment_views.Comments.as_view()),
    path("comment/<int:comment_pk>", comment_views.Comment.as_view()),
]
