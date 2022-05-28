from .serializers import GetUserSerializer, CreateUserSerializer, TokenSerializer
from rest_framework.authtoken.models import Token
from django.conf import settings
from .models import User, Verification
from .constants import send_sms_url, confirmed
import phonenumbers as pns
from random import randint
from requests import get


def start_new_verification(payload: str) -> tuple:
    if not is_valid_phone(payload):
        return {
                'error': 'invalid phone number',
                'success': False,
            }, 400

    if User.objects.filter(phone=payload).exists():
        return {
            'error': 'user with that phone number already exists',
            'success': False
            }, 409

    if Verification.objects.filter(phone=payload).exists():
        Verification.objects.get(phone=payload).delete()
    
    verification = Verification.objects.create(phone=payload, code=randint(1000, 9999))

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
    return {
        'success': True,
        'verification': {
            'phone': verification.phone,
            'code': verification.code
        }
    }, 201
    # else:
    #     verification.delete()
    #     return data, response.status_code


def verification(number: str, code: str) -> tuple:
    if not is_valid_phone(number):
        return {
                'error': 'invalid phone number',
                'success': False,
            }, 400

    if not Verification.objects.filter(phone=number, code=code).exists():
        return {
            'error': 'does not seem that phone and code match together',
            'success': False
        }, 404
    
    verification = Verification.objects.get(phone=number, code=code)
    verification.code = confirmed
    verification.save()

    return {
        'success': True,
        'message': 'verification went successfully'
    }, 200


def is_valid_phone(payload: str) -> bool:
    try:
        if pns.is_possible_number(pns.parse(payload)):
            return True
    except:
        return False


def create_verified_user(info: dict) -> tuple:
    user_serializer = CreateUserSerializer(data=info, many=False)
    
    if user_serializer.is_valid():
        user = user_serializer.create(user_serializer.validated_data)
        user.save()
    else:
        return user_serializer.errors, 400

    # verification.delete()

    token = Token.objects.get(user=user)
    token_serializer = TokenSerializer(token, many=False)

    return {
            'user': user_serializer.data,
            'token': token_serializer.data
        }, 201
