from .serializers import UserSerializer, TokenSerializer, VerificationSerializer
from rest_framework.authtoken.models import Token
from apps.api.models import Photo
from django.conf import settings
from .models import Verification
from .constants import send_sms_url, confirmed
from requests import get
from random import randint


def start_new_verification(payload: str) -> tuple:
    if Verification.objects.filter(phone=payload).exists():
        Verification.objects.get(phone=payload).delete()

    serializer = VerificationSerializer(data={'phone': payload, 'code': randint(1000, 9999)}, many=False)
    
    if serializer.is_valid():
        verification = serializer.create(serializer.validated_data)
    else:
        return serializer.errors, 400

    response = get(
        url=send_sms_url,
        params={
            'apiKey': settings.API_KEY,
            'recipient': verification.phone,
            'text': f'GameRoom account verification code: {verification.code}'
        }
    )

    data = response.json()

    # if data.get('code') is 0:
    verification.save()
    return serializer.data, 201
    # else:
    #     verification.delete()
    #     return data, response.status_code


def verify(payload: dict) -> tuple:
    try:
        verification = Verification.objects.get(phone=payload.get('phone'))
    except Verification.DoesNotExist:
        return {'phone': ['Does not exist in verification table']}, 404
    
    if verification.code == confirmed:
        return {'phone': ['Already verified']}, 400

    elif verification.code == payload.get('code'):
        verification.code = confirmed
        verification.save()
        return {'phone': ['Successfully verified']}, 200

    else:
        return {'phone': ['Phone and code does not match together']}, 404


def create_verified_user(info: dict) -> tuple:
    user_serializer = UserSerializer(data=info, many=False)
    
    if user_serializer.is_valid():
        user = user_serializer.create(user_serializer.validated_data)
        user.save()
    else:
        return user_serializer.errors, 400

    token = Token.objects.get(user=user)
    token_serializer = TokenSerializer(token, many=False)

    return {
            'user': user_serializer.data,
            'token': token_serializer.data
        }, 201
