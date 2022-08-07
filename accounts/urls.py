from django.urls import path
from accounts import views as user_views

app_name = "accounts"

urlpatterns = [
    path("signup", user_views.SignupView.as_view()),
    path("login", user_views.LoginView.as_view()),
    path("kakao-login", user_views.KakaoLoginView.as_view()),
    path("kakao-login/callback", user_views.KakaoCallBackView.as_view()),
    #path("google-login", user_views.GoogleLoginView.as_view()),
]
