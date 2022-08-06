from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from accounts.swagger import swagger_utils, swagger_ser
from accounts import serializers as account_serializers
from accounts import utils

class SignupView(APIView):

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



class LoginView(APIView):
    pass