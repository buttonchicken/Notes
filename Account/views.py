from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class Login(APIView):
    def post(self,request):
        try:
            username = request.data['username']
            password = request.data['password']
            user=authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({"success": True, "message": "Login successful",
                                 'refresh': str(refresh),
                                 'access': str(refresh.access_token)},
                                 status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"success":False,"message":"Invalid password"},
                             status=status.HTTP_400_BAD_REQUEST)    
        except:
            return Response({"success":False,"message":"Please enter username and password"},
                             status=status.HTTP_400_BAD_REQUEST)

class Register(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        usr_obj = User.objects.filter(username=username)
        if len(usr_obj)>0:
            return Response({"success":False,"message":"username already exists"},status=status.HTTP_400_BAD_REQUEST)
        else:
            usr = User()
            usr.username=username
            usr.set_password(password)
            usr.save()
            refresh = RefreshToken.for_user(usr)
            return Response({"success": True, "message": "Login successful",
                            'refresh': str(refresh),
                            'access': str(refresh.access_token)},
                            status=status.HTTP_202_ACCEPTED)