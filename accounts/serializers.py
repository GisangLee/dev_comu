from rest_framework.serializers import ModelSerializer, CharField
from django.db.models import Q
from accounts import models as account_models

class SignupSerializer(ModelSerializer):
    password = CharField(write_only=True)

    def create(self, validated_data):
        if validated_data["email"] and validated_data["username"]:

            try:
                already_existed_user = account_models.User.objects.get( Q(email=validated_data["email"]) | Q(username=validated_data["username"]) )

                if already_existed_user:
                    
                    return None

            except account_models.User.DoesNotExist:

                req_password = validated_data.pop("password")
                user = account_models.User.objects.create(**validated_data)
                user.set_password(req_password)
                user.save()
                return user

    class Meta:
        model = account_models.User
        fields = (
            "pk",
            "username",
            "email",
            "birthdate",
            "password",
        )
