from rest_framework import serializers
from .models import User, Todolist

class TodolistSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todolist
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
        extra_kwargs={'password':{'write_only':True}}

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()