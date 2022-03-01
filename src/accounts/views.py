import re
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from . import serializers as user_serializers
from . import models as user_models


class UserView(APIView):
    def get(self, request):
        return Response({"message": "OK"}, status=status.HTTP_200_OK)


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        res = None
        res_status = None

        profile_photo = request.FILES.getlist("profile")[0]

        try:
            user = user_models.User.objects.prefetch_related("profile").get(
                email=request.data["email"]
            )
            if user:
                res = {"message": "이미 등록된 이메일입니다."}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except user_models.User.DoesNotExist:
            pattern = re.compile("^[a-z0-9+]*$")

            if pattern.search(request.data["username"]) == None:
                response = {"message": "영문 소문자 및 숫자만 입력가능 합니다."}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = user_models.User.objects.prefetch_related("profile").get(
                    username=request.data["username"]
                )
                if user:
                    res = {"message": "이미 등록된 이름입니다."}
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            except user_models.User.DoesNotExist:
                serializer = user_serializers.SignupSerializer(data=request.data)

                if serializer.is_valid():
                    if profile_photo:
                        user = serializer.save()
                        profile = user_models.UseProfile.objects.create(
                            user=user, file=profile_photo
                        )
                        profile.save()
                    else:
                        user = serializer.save()
                    res = {"message": "회원가입 완료"}
                    res_status = status.HTTP_200_OK
                else:
                    res = {"message": "회원가입 불가"}
                    res_status = status.HTTP_400_BAD_REQUEST
                return Response(res, status=res_status)
