from enum import Enum


class AccountsErrorMessages(Enum):
    not_exist = 'пользователя с таким телефонным номером не существует'
    exists = 'пользователь с таким телефонным номером уже существует'
    invalid_info = 'введенная информация не подходит по формату'


class AccountsSuccessMessages(Enum):
    created = 'аккаунт успешно создан'


class AccountsRoutes(Enum):
    sign_up = 'sign-up'
    sign_in = 'sign-in'


CONFIRMED = 'confirmed'
