from .models import Telegram
from telebot import types


class Emoji:
    football = '⚽'
    heart = '❤️'
    explosion = '💥'
    bomb = '💣'
    rocket = '🚀'
    fire = '🔥'
    commet = '☄️'
    lightning = '⚡'
    danger = '⚠️'
    stop = '🚫'


class Start:
    name = 'start'
    command = '/start'
    message = 'Добро пожаловать, футболист!\nЗдесь ты можешь зарегистрироваться на игру или посмотреть историю своих матчей'

class Profile:
    name = 'profile'
    command = '/profile'
    button_text = 'Профиль'

    def message(self, user: Telegram):
        text = 'Ваш профиль:\n'
        text += f'username: {user.username}\n'
        text += f'first_name: {user.first_name}\n'
        text += f'last_name: {user.last_name}\n'
        text += f'age: {user.age}\n'
        text += f'phone: {user.phone}\n'

        return text


    button = types.InlineKeyboardButton(
        text=button_text,
        callback_data=name
    )

class Edit:
    name = 'edit'
    command = '/edit'
    message = 'Выберите какую информацию профиля редактировать'
    button_text = 'Редактировать профиль'

    button = types.InlineKeyboardButton(
        text=button_text,
        callback_data=name
    )


# class Commands:
#     start = 'start'
#     test = 'test'
#     edit = 'update'
#     profile = 'profile'
#     games = 'games'


# class Messages:
#     start = 'Добро пожаловать, футболист!\nЗдесь ты можешь зарегистрироваться на игру или посмотреть историю своих матчей'
#     test = 'Test'
#     edit = 'Введите эту информацию'
#     profile = 'Вот ваш профиль:'
#     games = 'Список всех активных игр:'


# class ButtonTexts:
#     start = 'Start'
#     test = 'Test Text'
#     edit = 'Заполнить профиль'
#     profile = 'Профиль'
#     games = 'Игры'
