from django.core.management.base import BaseCommand
from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot import TeleBot
from django.conf import settings
from ... import constants as const
from ... import models


bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


@bot.message_handler([const.Commands.start])
def start(message):
    user, created  = models.Telegram.objects.get_or_create(
        id=message.from_user.id,
        defaults={
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name
        }
    )

    markup = InlineKeyboardMarkup()

    # if created:
    fill_profile = InlineKeyboardButton(
        text=const.ButtonTexts.profile,
        callback_data=const.Commands.profile
    )
    markup.add(fill_profile)
    # else:
    #     pass

    bot.send_message(
        chat_id=message.chat.id, 
        text=const.Messages.start,
        reply_markup=markup,
        parse_mode='html'
    )


@bot.callback_query_handler(func=lambda call: True)
def query_callback(call):
    match call.data:
        case const.Callbacks.profile:
            profile()


@bot.message_handler([const.Commands.test])
def test(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=const.Messages.test,
        parse_mode='html'
    )


@bot.message_handler([const.Commands.profile])
def profile(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Profile'
    )


class Command(BaseCommand):
    help = 'Telegram bot setup command '

    def handle(self, *args, **kwargs):
        print('Telegram bot started')
        # bot.infinity_polling()
        bot.polling(none_stop=False, interval=0)
