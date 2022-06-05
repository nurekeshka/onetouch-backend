from .serializers import UserSerializer, TokenSerializer
from rest_framework.authtoken.models import Token  


def create_verified_user(info: dict) -> tuple:
    user_serializer = UserSerializer(data=info, many=False)
    
    if user_serializer.is_valid():
        user = user_serializer.create(user_serializer.validated_data)
        user.set_password(info['password'])
        user.save()
    else:
        return user_serializer.errors, 400

    token = Token.objects.get(user=user)
    token_serializer = TokenSerializer(token, many=False)

    return {
            'user': user_serializer.data,
            'token': token_serializer.data
        }, 201
