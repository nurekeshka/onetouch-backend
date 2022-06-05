from .serializers import PhoneVerificationSerializer
from apps.accounts.constants import confirmed
from .constants import send_sms_url
from .models import PhoneVerification
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
        return serializer.errors, 400

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
    return serializer.data, 201
    # else:
    #     verification.delete()
    #     return data, response.status_code


def verify(payload: dict) -> tuple:
    try:
        verification = PhoneVerification.objects.get(phone=payload.get('phone'))
    except PhoneVerification.DoesNotExist:
        return {'phone': ['Does not exist in verification table']}, 404
    
    if verification.code == confirmed:
        return {'phone': ['Already verified']}, 400

    elif verification.code == payload.get('code'):
        verification.update(code=confirmed)
        return {'phone': ['Successfully verified']}, 200

    else:
        return {'phone': ['Phone and code does not match together']}, 404
