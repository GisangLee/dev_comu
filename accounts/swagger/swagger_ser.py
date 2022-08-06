from rest_framework.serializers import ModelSerializer, Serializer, CharField, BooleanField, DateField
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from accounts.jwt import generate
from accounts import models as account_models

class SignupSerializer(ModelSerializer):
    password = CharField(write_only=True)
    birthdate = DateField(write_only=True)
    gender = CharField(write_only=True)

    def create(self, validated_data):
        if validated_data["email"] and validated_data["username"]:
            req_password = validated_data.pop("password")
            user = account_models.User.objects.create(**validated_data)
            user.set_password(req_password)
            user.save()
            return user

    class Meta:
        model = account_models.User
        fields = (
            "pk",
            "email",
            "username",
            "password",
            "birthdate",
            "gender",
        )


class LoginSerializer(Serializer):
    username = CharField(max_length=320, help_text="이메일 OR ID")
    password = CharField(max_length=128, write_only=True, help_text="비밀번호")

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            response = {
                "message": "등록된 이름(ID)가 없습니다",
                "token": None,
                "status": 401,
            }
            return response

        payload = {
            "user_id": user.id,
        }

        access_jwt = generate.generate_jwt_token(payload, "access")
        update_last_login(None, user)

        response = {
            "message": "OK",
            "token": access_jwt,
            "status": 200,
            "username": user.username,
            "email": user.email,
        }
        return response