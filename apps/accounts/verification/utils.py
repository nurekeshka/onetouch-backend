from .serializers import PhoneVerificationSerializer
from apps.accounts.constants import confirmed
from .constants import send_sms_url
from .models import PhoneVerification
from rest_framework import status
from django.conf import settings
from random import randint
from requests import get


def start_new_verification(payload: str) -> tuple:
    if PhoneVerification.objects.filter(phone=payload).exists():
        PhoneVerification.objects.get(phone=payload).delete()

    serializer = PhoneVerificationSerializer(data={'phone': payload, 'code': randint(1000, 9999)}, many=False)
    
    if serializer.is_valid():
        verification = serializer.create(serializer.validated_data)
    else:
        return serializer.errors, status.HTTP_400_BAD_REQUEST

    response = get(
        url=send_sms_url,
        params={
            'apiKey': settings.SMS_API_KEY,
            'recipient': verification.phone,
            'text': f'GameRoom account verification code: {verification.code}'
        }
    )

    data = response.json()

    # if data.get('code') is 0:
    verification.save()
    return serializer.data, status.HTTP_201_CREATED
    # else:
    #     verification.delete()
    #     return data, response.status_code


def verify(payload: dict) -> tuple:
    try:
        verification = PhoneVerification.objects.get(phone=payload.get('phone'))
    except PhoneVerification.DoesNotExist:
        return {'phone': ['Does not exist in verification table']}, status.HTTP_404_NOT_FOUND
    
    if verification.code == confirmed:
        return {'phone': ['Already verified']}, status.HTTP_400_BAD_REQUEST

    elif verification.code == payload.get('code'):
        verification.code = confirmed
        verification.save()
        return {'phone': ['Successfully verified']}, status.HTTP_200_OK

    else:
        return {'phone': ['Phone and code does not match together']}, status.HTTP_404_NOT_FOUND
