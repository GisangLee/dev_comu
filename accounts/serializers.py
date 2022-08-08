from rest_framework.serializers import ModelSerializer, CharField, Serializer, SerializerMethodField
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from accounts import models as account_models
from accounts.jwt import generate


class ProfileImageSerializer(ModelSerializer):

    class Meta:
        model = account_models.UserProfile
        fields = ("pk", "avatar",)


class UserSerializer(ModelSerializer):
    profile_images = SerializerMethodField()

    def get_profile_images(self, obj):

        image = obj.profile_images.all().last()

        return ProfileImageSerializer(image).data

    class Meta:
        model = account_models.User
        fields = ("pk", "username", "email", "profile_images",)

class UserSerializerForLikedOrDisliked(ModelSerializer):

    class Meta:
        model = account_models.User
        fields = ("pk")



class LoginSerializer(Serializer):
    username = CharField(max_length=320)
    password = CharField(max_length=128, write_only=True)
    
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        print(f"username: {username}")
        print(f"password: {password}")
        user = authenticate(username=username, password=password)

        if user is None:
            response = {
                "message": "등록된 이름(ID)가 없습니다",
                "token": None,
                "status": 400,
            }
            return response

        if not user.check_password(password):
        
            response = {
                "message": "비밀번호가 일치하지 않습니다.",
                "token": None,
                "status": 400,
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
            "user_id": user.id
        }
        return response



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
            "gender",
            "login_method"
        )
