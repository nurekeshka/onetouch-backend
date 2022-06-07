from django.core.management.base import BaseCommand
from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot import TeleBot
from django.conf import settings
from ... import constants as const
from ...models import Telegram


bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


def telegram_user(function):
    def inner(message):
        user, created  = Telegram.objects.get_or_create(
            id=message.from_user.id,
            defaults={
                'username': message.from_user.username,
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name
            }
        )
        function(message, user, created)
    return inner


@bot.message_handler([const.Commands.start])
@telegram_user
def start(message, user, created):
    markup = InlineKeyboardMarkup()

    if created or not user.is_active():
        markup.add(
            InlineKeyboardButton(
                text=const.ButtonTexts.update,
                callback_data=const.Commands.update
            )
        )
    else:
        markup.add(
            InlineKeyboardButton(
                text=const.ButtonTexts.profile,
                callback_data=const.Commands.profile
            ),
            InlineKeyboardButton(
                text=const.ButtonTexts.games,
                callback_data=const.Commands.games
            )
        )

    bot.send_message(
        chat_id=message.chat.id, 
        text=const.Messages.start,
        reply_markup=markup,
        parse_mode='html'
    )


@bot.callback_query_handler(func=lambda call: True)
def query_callback(call):
    match call.data:
        case const.Commands.update:
            user = Telegram.objects.get_or_create

            bot.send_message(
                chat_id=call.message.chat.id,
                text='Введите свой возраст'
            )


# @bot.message_handler([const.Commands.test])
# def test(message):
#     bot.send_message(
#         chat_id=message.chat.id,
#         text=const.Messages.test,
#         parse_mode='html'
#     )


class Command(BaseCommand):
    help = 'Telegram bot setup command '

    def handle(self, *args, **kwargs):
        print('Telegram bot started')
        # bot.infinity_polling()
        bot.polling(none_stop=False, interval=0)
