import os, jwt, time, datetime
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.backends import ModelBackend
from accounts import models as user_models

# 이메일 + 유저 ID 둘다 로그인 되도록 하는 커스텀 인증 시스템 구축
# 이메일 + 유저 ID 둘다 로그인 되도록 하는 커스텀 인증 시스템 구축
class EmailUsernameLoginBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None):
        if '@' in username:
            kwargs = {
                "email": username
            }
        else:
            kwargs = {
                "username": username
            }
        try:
            #user = get_user_model().objects.get(**kwargs)
            user = user_models.User.objects.get(**kwargs)

            if user:
                return user

        except user_models.User.DoesNotExist:
            return None

    def get_user_model():
        """
        Return the User model that is active in this project.
        """
        try:
            return django_apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)
        except ValueError:
            raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
        except LookupError:
            raise ImproperlyConfigured(
                "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
            )

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None