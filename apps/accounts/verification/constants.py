from enum import Enum


class VerificationErrorMessages(Enum):
    not_exist_phone = 'активная верификация этого телефонного номера не существует в базе данных'
    verified = 'телефонный номер уже подтвержден, быстрее создавайте аккаунт'
    not_verified = 'телефонный номер еще не подтвержден'
    invalid_code = 'неверный код подтверждения'
    invalid_phone = 'формат телефонного номера не правильный. Он должен содержать: код страны, национальный номер и быть длинной в 12 символов'
    none_phone = 'телефонный номер не указан в запросе'


class VerificationSuccessMessages(Enum):
    send_sms_code = 'сообщение с кодом подтверждения было выслано на ваш номер'
    verified = 'телефонный номер успешно подтвержден'


class VerificationRoutes(Enum):
    create = 'create_verification'
    verify = 'verify_verification'


MOBIZON_URL = 'https://api.mobizon.kz/service/Message/SendSmsMessage'
MOBIZON_SMS_TEXT = 'Alpha-Sports account verification code: {0}'

PHONE_CLEANING_TABLE = str.maketrans({x: '' for x in ('(', ' ', ')', '-')})
