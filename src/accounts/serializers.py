from rest_framework import serializers
from . import models as user_models


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
