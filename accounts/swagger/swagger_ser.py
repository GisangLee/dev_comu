from rest_framework.serializers import ModelSerializer, Serializer, CharField, BooleanField, DateField
from django.contrib.auth import authenticate
#from django.contrib.auth.models import update_last_login
#from accounts.auth import generate_token as jwt_tokens
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