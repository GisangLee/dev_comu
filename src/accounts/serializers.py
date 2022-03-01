from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from . import models as user_models
from accounts.jwt import tokens as jwt_tokens


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=320)
    password = serializers.CharField(max_length=128, write_only=True)

    response = None

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            response = {
                "message": "등록된 이름이 없습니다",
                "token": None,
                "status": 400,
            }
            return response

        elif user.login_try >= 5:
            response = {
                "message": "비밀번호가 5회이상 틀려 로그인 할수 없습니다. 비밀번호찾기를 이용해주세요.",
                "token": None,
                "login_try": user.login_try,
                "status": 400,
            }
            return response

        elif user.is_wrong_pwd:
            response = {
                "message": "비밀번호가 맞지 않아요. 다시 확인해주세요.",
                "token": None,
                "login_try": user.login_try,
                "status": 400,
            }
            return response

        payload = {
            "user_id": user.id,
        }

        access_jwt = jwt_tokens.generate_jwt_token(payload, "access")
        update_last_login(None, user)

        response = {
            "message": "OK",
            "token": access_jwt,
            "login_try": user.login_try,
            "status": 200,
        }
        return response


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        if validated_data["email"] and validated_data["username"]:
            req_password = validated_data.pop("password")
            user = user_models.User.objects.create(**validated_data)
            user.set_password(req_password)
            user.save()
            return user

    class Meta:
        model = user_models.User
        fields = ("pk", "username", "email", "password")
