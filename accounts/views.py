from curses import reset_prog_mode
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from accounts import utils
from accounts import perms
from accounts.swagger import swagger_utils, swagger_ser
from accounts import serializers as account_serializers

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