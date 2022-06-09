from telebot import types


class Start:
    name = 'start'
    command = '/start'
    message = 'Добро пожаловать, футболист!\nЗдесь ты можешь зарегистрироваться на игру или посмотреть историю своих матчей'

class Profile:
    name = 'profile'
    command = '/profile'
    message = 'Вот ваш профиль:'
    text = 'Профиль'

    button = types.InlineKeyboardButton(
        text=text,
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
