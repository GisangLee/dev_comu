from django.urls import path
from . import views as user_views

app_name = "accounts"

urlpatterns = [
    path("user", user_views.UserView.as_view()),
    # path('admin/', admin.site.urls),
]
