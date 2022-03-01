from django.conf import settings
from django.contrib.auth import get_user_model
from accounts import models as user_models
from django.contrib.auth.backends import ModelBackend


class EmailUsernameLoginBackend:
    def authenticate(self, request, username=None, password=None):
        if "@" in username:
            kwargs = {"email": username}
        else:
            kwargs = {"username": username}
        try:
            user = get_user_model().objects.get(**kwargs)

            if user.check_password(password):
                user.is_wrong_pwd = False
                user.login_try = 0
                user.save()
                return user

            else:
                # 비밀번호 오류 시 로그인 시도 횟수 증가
                user.login_try = user.login_try + 1
                user.is_wrong_pwd = True
                user.save()
                return user

        except user_models.User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
