from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class SignupView(APIView):

    def get(self, request):

        res = {
            "action": "회원가입",
            "method": "POST",
            "req_url": "/accounts/signup",
            "message": "회원가입"
        }

        return Response(res, status = status.HTTP_200_OK)

"""
    @swagger_auto_schema(request_body=swagger_serializers.SignupSerializer, manual_parameters=swagger_utils.login_no_require, tags=["회원가입"])
    def post(self, request):

        # 회원가입 진행
        serializer = account_serializer.SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            # DB에 저장
            serializer.save()
            res = {
                "action": "회원가입",
                "method": "POST",
                "message": serializer.data,
                "status": "success"
            }
            return Response(res, status=status.HTTP_201_CREATED)

        res = {
            "action": "회원가입",
            "method": "POST",
            "message": serializer.errors,
            "status": "fail"
        }

        return Response(res, status=status.HTTP_400_BAD_REQUEST)
"""


class LoginView(APIView):
    pass