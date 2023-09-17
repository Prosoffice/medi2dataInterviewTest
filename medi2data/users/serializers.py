from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField()
