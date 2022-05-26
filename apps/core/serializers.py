from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'photo', 'phone')

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('user', 'key')
