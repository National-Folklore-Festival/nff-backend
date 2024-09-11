from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create your views here.
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

        return Response({})

