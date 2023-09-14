from apps.accounts.models import User
from .constants import PHONE_CLEANING_TABLE
from .constants import MOBIZON_URL
from .constants import MOBIZON_SMS_TEXT
from .models import PhoneVerification
from django.conf import settings
from random import randint
from requests import get


def get_phone_verification(phone: str) -> PhoneVerification:
    return PhoneVerification.objects.get(phone=phone)


def create_random_code() -> str:
    return randint(1000, 9999)


def verification_exists(phone: str) -> bool:
    return PhoneVerification.objects.filter(phone=phone).exists()


def account_exists(phone: str) -> bool:
    return User.objects.filter(phone=phone).exists()


def delete_verification(phone: str) -> PhoneVerification:
    return PhoneVerification.objects.get(phone=phone).delete()


def send_confirmation_code(phone: str, code: str) -> dict:
    return get(
        url=MOBIZON_URL,
        params={'apiKey': settings.SMS_API_KEY,
                'recipient': phone,
                'text': MOBIZON_SMS_TEXT.format(code)
                }
    ).json()


def format_phone(payload: str) -> str:
    return payload.translate(PHONE_CLEANING_TABLE)
