from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate, login, logout


class UserRegistration(APIView):
    def post (self, request):
        register_data = RegisterSerializer(data=request.data)
        register_data.is_valid(raise_exception=True)
        new_user = register_data.save()
        token = Token.objects.create(user=new_user) 

        return Response({"token": token.key, "user": register_data.data}, status=status.HTTP_201_CREATED)

class UserLogin(APIView):
    def post(self, request):
        login_data = LoginSerializer(data=request.data)
        login_data.is_valid(raise_exception=True)

        username = login_data.validated_data['username']
        password = login_data.validated_data['password']

        user = authenticate(username=username ,password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({"token":token.key, "username":user.username}, status = status.HTTP_200_OK)

        else:
            return Response({"message":"Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
            
class UserLogout(APIView):    
    def get(self,request):
        logout(request)
        return Response({"message": "Logout success"})