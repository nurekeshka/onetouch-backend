from .serializers import UserSerializer, TokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status


def get_user_token(user) -> Token:
    return Token.objects.get(user=user)
