from apps.common.games.models import Game
from .models import Telegram
from .constants import Emoji
from telebot import types


class Start:
    name = 'start'
    message = 'Добро пожаловать, футболист!\nЗдесь ты можешь зарегистрироваться на игру или посмотреть историю своих матчей'


class Menu:
    name = 'menu'
    
    def message(user: Telegram):
        text = f'Привет {user.username}! '
        text += 'Куда отправимся?'
        return text

    def markup(user: Telegram):
        inline = types.InlineKeyboardMarkup()

        if user.is_active():
            inline.add( Profile.button, Games.button )
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
                    callback_data=f'edit:{value}'
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
    button = types.InlineKeyboardButton(
        text='Игры',
        callback_data=name
    )

    def message():
        text = Emoji.football.value + _bold(' Все игры на ближайшее время ') + Emoji.football.value + '\n\n'
        return text
    
    def markup():
        inline = types.InlineKeyboardMarkup(
            keyboard=None,
            row_width=1
        )

        games = list()

        for game in Game.objects.all():
            if game.is_today():
                games.append(
                    types.InlineKeyboardButton(
                        text=str(game),
                        callback_data=f'game:{game.id}'
                    )
                )
        
        inline.add(*games)
        inline.add( types.InlineKeyboardButton(
                text=Back.text,
                callback_data=Menu.name
            ) 
        )

        return inline


class GameDetailed:
    
    def message(game: Game):
        text = 'Более подробная информация об игре\n\n'
        
        for key, value in game.detailed().items():
            text += f'{_bold(key.title())}: {value}\n'
        
        return text

    def markup(game: Game):
        inline = types.InlineKeyboardMarkup(
            keyboard=None,
            row_width=1
        )

        for team in game.teams():
            inline.add(
                types.InlineKeyboardButton(
                    text=team.name,
                    callback_data=f'sign-in:{team.id}'
                )
            )

        inline.add(
            types.InlineKeyboardButton(
                text=Back.text,
                callback_data=Games.name
            )
        )

        return inline


class Back:
    text = '« Вернуться назад'


class Save:
    text = 'Сохранено'


def _bold(text: str) -> str:
    return '<b>' + str(text) + '</b>'
