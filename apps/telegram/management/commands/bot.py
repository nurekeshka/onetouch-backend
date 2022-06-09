from apps.accounts.verification.serializers import PhoneVerificationSerializer
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import Telegram
from ...utils import telegram_user
from ...interface import *
from telebot import types
from telebot import TeleBot


bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)

@bot.message_handler(commands=[Start.name])
@telegram_user
def start(message: types.Message, user: Telegram):
    bot.send_message(
        chat_id=message.chat.id, 
        text=Start.message,
        reply_markup=Menu.markup(user),
        parse_mode='html'
    )


@bot.message_handler(commands=[Profile.name])
@telegram_user
def profile(message: types.Message, user: Telegram):
    bot.send_message(
        chat_id=message.chat.id,
        text=Profile.message(user),
        reply_markup=Profile.markup(user),
        parse_mode='html'
    )


@bot.message_handler(commands=[Games.name])
def games(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=Games.message(),
        reply_markup=Games.markup(),
        parse_mode='html'
    )


@bot.callback_query_handler(func=lambda call: True)
@telegram_user
def callback_handler(call: types.CallbackQuery, user: Telegram):
    match call.data:
        case Menu.name:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text=Menu.message,
                parse_mode='html'
            )
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=Menu.markup(user)
            )

        case Profile.name:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text=Profile.message(user),
                parse_mode='html'
            )
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=Profile.markup(user)
            )

        case _:
            bot.send_message(
                chat_id=call.message.chat.id,
                text=call.data,
                parse_mode='html'
            )

class Command(BaseCommand):
    help = 'Telegram bot setup command '

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        # bot.polling(non_stop=False)
        bot.infinity_polling()
