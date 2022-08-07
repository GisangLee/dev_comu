import os, requests, datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import update_last_login
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from accounts import utils
from accounts import perms
from accounts.swagger import swagger_utils, swagger_ser
from accounts.jwt import generate
from accounts import serializers as account_serializers
from accounts import models as user_models

# 회원가입
class SignupView(APIView):
    permission_classes = [perms.AllowAny]

    @swagger_auto_schema(request_body=swagger_ser.SignupSerializer, manual_parameters=swagger_utils.login_no_require, tags=["회원가입"])
    def post(self, request):

        # 회원가입 진행
        serializer = account_serializers.SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            # DB에 저장
            serializer.save()

            res = utils.api_response(action="회원가입", method="POST", error="", message=serializer.data, status="success", url="/accounts/signup")

            return Response(res, status=status.HTTP_201_CREATED)

        res = utils.api_response(action="회원가입", method="POST", error=serializer.errors, message="", status="fail", url="/accounts/signup")

        return Response(res, status=status.HTTP_400_BAD_REQUEST)


# 기본 이메일 로그인
class LoginView(APIView):
    permission_classes = [perms.AllowAny]

    @swagger_auto_schema(request_body=swagger_ser.LoginSerializer, manual_parameters=swagger_utils.login_no_require, tags=["로그인"])
    def post(self, request):

        serializer = account_serializers.LoginSerializer(data=request.data)
        
        if not serializer.is_valid():

            res = utils.api_response(action="로그인", method="POST", error="로그인 실패", message="", url="/accounts/login", status="fail")
            
            # res = {
            #     "action": "로그인",
            #     "method": "POST",
            #     "message": "로그인 실패",
            #     "token": None,
            #     "user": None,
            # }
            
            res_status = status.HTTP_400_BAD_REQUEST

            return Response(res, status=res_status)

        # 정상 로그인
        else:
            res_status = None

            # 직렬화 로직 예외 처리
            if serializer.validated_data["status"] == 400:
                res_status = status.HTTP_400_BAD_REQUEST

                res = utils.api_response(action="로그인", method="POST", error=serializer.validated_data, message="", url="/accounts/login", status="fail")

                return Response(res, res_status)

            else:
                res_status = status.HTTP_200_OK

                res = utils.api_response(action="로그인", method="POST", error="", message=serializer.validated_data, url="/accounts/login", status="success")

                return Response(res, res_status)


# 카카오 로그인
class KakaoLoginView(APIView):

    permission_classes = [perms.AllowAny]

    @swagger_auto_schema(manual_parameters=swagger_utils.login_no_require, tags=["카카오 로그인"])
    def get(self, request):
        REST_API_KEY = os.environ.get("KAKAO_REST_API_KEY")
        local_callback_uri = "http://127.0.0.1:8000/api-v1/accounts/kakao-login/callback"

        redirect_uri = f"kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={local_callback_uri}&response_type=code&prompt=login"
        return redirect(f"https://{redirect_uri}")


class KakaoCallBackView(APIView):
    permission_classes = [perms.AllowAny]

    @swagger_auto_schema(manual_parameters=swagger_utils.login_no_require, tags=["카카오 로그인 콜백"])
    def get(self, request):
        REST_API_KEY = os.environ.get("KAKAO_REST_API_KEY")
        local_callback_uri = "http://127.0.0.1:8000/api-v1/accounts/kakao-login/callback"

        code = request.GET.get("code")

        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={local_callback_uri}&code={code}"
        )

        token_response_json = token_request.json()
        access_token = token_response_json.get("access_token")

        # 카카오 프로필 정보 가져오기
        profile_request = requests.get(
            f"https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        
        profile_json = profile_request.json()

        email = profile_json.get("kakao_account").get("email", None)

        properties = profile_json.get("properties")
        username = properties.get("nickname")

        gender = profile_json.get("kakao_account").get("gender")
        profile_image = profile_json.get("kakao_account")
        profile_image = profile_image.get("profile").get("profile_image_url")
        birthday = profile_json.get("kakao_account").get("birthday")

        if gender == "male":
            gender = "M"

        else:
            gender = "F"

        try:
            user = user_models.User.objects.prefetch_related("profile_images").get(email=email)
            if user:
                if not user.is_deleted and user.login_method == user_models.User.LOGIN_KAKAO:
                    payload = {"user_id": user.id}

                    jwt_token = generate.generate_jwt_token(payload, "access")

                    response = {
                        "message": "카카오 계정으로 로그인 되었습니다.",
                        "jwt_token": jwt_token,
                        "kakao_access_token": access_token,
                        "user": user.username,
                    }
                    update_last_login(None, user)
                    return Response(response, status=status.HTTP_200_OK)

                elif not user.is_deleted and user.login_method != user_models.User.LOGIN_KAKAO:
                    response = {
                        "message": f"{user.login_method} 계정으로 이미 존재하는 계정입니다.",
                    }
                    return Response(response, status=status.HTTP_200_OK)

        except user_models.User.DoesNotExist:
            user = user_models.User.objects.create(email=email, username=username)
            user.login_method = "kakao"
            user.email_verified = True
            user.gender = gender
            user.birthdate = birthday
            user.set_unusable_password()
            user.save()

            if profile_image is not None:

                avatar = requests.get(profile_image)
                user_profile = user_models.UserProfile.objects.create(user=user)
                user_profile.avatar.save(
                    f"{username}-avatar.png", ContentFile(avatar.content)
                )
    
            payload = {"user_id": user.id}

            jwt_token = generate.generate_jwt_token(payload, "access")

            response = {
                "message": "카카오 계정으로 회원가입이 되었습니다.",
                "jwt_token": jwt_token,
                "kakao_access_token": access_token,
                "user_id": user.id,
            }

            update_last_login(None, user)

            return Response(response, status=status.HTTP_200_OK)




# 구글 로그인
class GoogleLoginView(APIView):
    permission_classes = [perms.AllowAny]

    def get(self, request):
        GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_REST_API_KEY")

        local_callback_uri = "http://127.0.0.1:8000/api-v1/accounts/google-login/callback"

        google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"
        scope = "https://www.googleapis.com/auth/userinfo.email "+ "https://www.googleapis.com/auth/userinfo.profile "+ "https://www.googleapis.com/auth/user.birthday.read "+ "https://www.googleapis.com/auth/user.gender.read "
        redirect_uri = f"{google_auth_api}?client_id={GOOGLE_CLIENT_ID}&response_type=code&redirect_uri={local_callback_uri}&scope={scope}"
        return redirect(redirect_uri)


class GoogleCallbackView(APIView):
    permission_classes = [perms.AllowAny]

    def get(self, request):
        code = request.GET.get("code")
        google_token_api = "https://oauth2.googleapis.com/token"
        GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_REST_API_KEY")
        GOOGLE_SECRET = os.environ.get("GOOGLE_SECRET_PASSWORD")

        local_callback_uri = "http://127.0.0.1:8000/api-v1/accounts/google-login/callback"

        state = "random_string"

        grant_type = "authorization_code"
        google_token_api += f"?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_SECRET}&code={code}&grant_type={grant_type}&&redirect_uri={local_callback_uri}&state={state}"
        token_response = requests.post(google_token_api)

        if not token_response.ok:
            raise ValueError("google_token is invalid")

        access_token = token_response.json().get("access_token")
        print(f"access_token: {access_token}")

        # 구글 프로필 정보 가져오기
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            params={"access_token": access_token},
        )

        if not user_info.ok:
            raise ValueError("사용자 정보를 불러오는데 실패했습니다.")

        user_info_json = user_info.json()

        profile = {
            "username": user_info_json.get("name"),
            "email": user_info_json["email"],
            "avatar": user_info_json.get("picture"),
            "email_verified": user_info_json.get("email_verified"),
        }

        try:
            user = user_models.User.objects.prefetch_related("profile_images").get(email=profile["email"])
            
            if not user.is_deleted and user.login_method == user_models.User.LOGIN_GOOGLE:
                payload = {"user_id": user.id}

                jwt_token = generate.generate_jwt_token(payload, "access")

                response = {
                    "message": "구글 계정으로 로그인 되었습니다.",
                    "jwt_token": jwt_token,
                    "user_id": user.id,
                }

                update_last_login(None, user)

                return Response(response, status=status.HTTP_200_OK)

            elif not user.is_deleted and user.login_method != user_models.User.LOGIN_GOOGLE:
                response = {
                    "message": f"{user.login_method} 계정으로 이미 존재하는 계정입니다.",
                }
                return Response(response, status=status.HTTP_200_OK)

        except user_models.User.DoesNotExist:
        
            user = user_models.User.objects.create(
                email=profile["email"], username=profile["username"]
            )

            if profile["avatar"] is not None:
                avatar = requests.get(profile["avatar"])
                user_profile = user_models.UserProfile.objects.create(user=user)
                user_profile.avatar.save(
                    f"{profile['username']}-avatar.png", ContentFile(avatar.content)
                )

            payload = {"user_id": user.id}

            user.login_method = "google"
            user.email_verified = profile["email_verified"]
            #user.pwd_change_date = datetime.datetime.now()
            user.set_unusable_password()
            user.save()

            jwt_token = generate.generate_jwt_token(payload, "access")

            response = {
                "message": "구글 계정으로 회원가입이 되었습니다.",
                "jwt_token": jwt_token,
                "user_id": user.id,
            }

            update_last_login(None, user)

            return Response(response, status=status.HTTP_200_OK)