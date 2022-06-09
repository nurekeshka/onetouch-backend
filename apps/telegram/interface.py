from apps.common.games.models import Game
from .models import Telegram
from .constants import Emoji
from telebot import types


class Start:
    name = 'start'
    message = 'Добро пожаловать, футболист!\nЗдесь ты можешь зарегистрироваться на игру или посмотреть историю своих матчей'


class Menu:
    name = 'menu'
    message = 'Вот меню. Что хотите сделать?'

    def markup(user: Telegram):
        inline = types.InlineKeyboardMarkup()

        if user.is_active():
            inline.add( Profile.button )
        else:
            inline.add( Profile.button )
        
        return inline


class Profile:
    name = 'profile'
    text = 'Профиль'
    button = types.InlineKeyboardButton(
        text=text,
        callback_data=name
    )

    def message(user: Telegram):
        text = Emoji.fire.value + _bold(' Вот ваш невероятный профиль ') + Emoji.fire.value + '\n\n'

        for key, value in user.info().items():
            if value is None:
                value = Emoji.stop.value
            text += f'{_bold(key.title())}: {value}\n'
        
        return text

    def markup(user: Telegram):
        inline = types.InlineKeyboardMarkup(keyboard=None, row_width=2)
        buttons = list()

        # Edit buttons
        for key, value in user.edit().items():
            buttons.append(
                types.InlineKeyboardButton(
                    text=f'Изменить {key}',
                    callback_data=value
                )
            )
        
        inline.add(*buttons)
        
        # Back button
        inline.add( types.InlineKeyboardButton(
                text=Back.text,
                callback_data=Menu.name
            ) 
        )
        
        return inline


class Games:
    name = 'games'
    text = 'Игры'
    button = types.InlineKeyboardButton(
        text=text,
        callback_data=name
    )

    def message(user: Telegram):
        text = Emoji.football.value + _bold(' Все игры на сегодня ') + Emoji.football.value + '\n\n'


class Back:
    text = '« Вернуться назад'


def _bold(text: str) -> str:
    return '<b>' + str(text) + '</b>'
