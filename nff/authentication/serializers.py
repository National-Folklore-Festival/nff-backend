from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
