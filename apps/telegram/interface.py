from apps.common.games.models import Game
from .constants import Emoji, MONTHES
from .models import Telegram
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
        teams = game.teams()

        text = f'{Emoji.voice.value} Игра #{game.pk}\n\n'
        text += f'{Emoji.calendar.value} {game.date.day} {MONTHES[game.date.month]}\n'
        text += f'{Emoji.marker.value} Адрес: {game.field.address}\n'
        text += f'{Emoji.clock.value} Время: {game.start.strftime("%H:%M")} - {game.end.strftime("%H:%M")}\n'
        text += f'{Emoji.people.value} Формат: {game.form - 1} + 1 ({len(teams)} команды)\n'
        text += f'{Emoji.money.value} С человека: ₸ {game.payment}\n'
        text += f'{Emoji.pencil.value} Запись по кнопке ниже\n'
        text += f'{Emoji.credit_card.value} Оплата тоже по кнопке ниже\n\n'
        
        for team in teams:
            text += f'{team.emoji} {team.name} ('
            players = team.players.all()

            if players:
                for player in players:
                    text += f'{player}, '
                text = text[:-2] + ')\n'
            else:
                text += '...)\n'


        text += f'\n{Emoji.running_guy.value} Осталось мест: {game.players_left()}'
        
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

    def media(game: Game):
        return game.field.photo.link


class Back:
    text = '« Вернуться назад'


class Edit:
    class first_name:
        message = 'Отправьте сообщение со своим именем'
    class last_name:
        message = 'Отправьте сообщение со своей фамилией'
    class age:
        message = 'Отправьте сообщение содержащее ваш возраст в цифрах'
        error = 'Возраст должен быть цифрой. Отправьте сообщение еще раз которое включает только цифры'
    class phone:
        message = 'Отправьте сообщение содержащее ваш телефонный номер'
        error = 'Телефонный номер не подходит по формату или уже существует пользователь с таким телефонным номером. Отправьте сообщение еще раз в формате:\n+7 *** *** ** **'


def _bold(text: str) -> str:
    return '<b>' + str(text) + '</b>'
