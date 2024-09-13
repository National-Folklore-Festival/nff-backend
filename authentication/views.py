from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class UserRegistration(APIView):
    def post (self, request):
        register_data = RegisterSerializer(data=request.data)
        if register_data.is_valid():
            new_user = register_data.save()

            token = Token.objects.create(user=new_user) 

            return Response({"token": token.key, "user": register_data.data}, status=status.HTTP_201_CREATED)
        return Response(register_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    def post(self, request):
        login_data = LoginSerializer(data=request.data)
        if login_data.is_valid():
            username = login_data.validated_data['username']
            password = login_data.validated_data['password']

            user = authenticate(username=username ,password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token":token.key, "username":user.username}, status = status.HTTP_200_OK)

            else:
                return Response({"message":"Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(login_data.errors, status=status.HTTP_400_BAD_REQUEST)

