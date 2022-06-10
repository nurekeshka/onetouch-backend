from apps.accounts.verification.serializers import PhoneVerificationSerializer
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import Telegram
from ...utils import telegram_user
from ...interface import *
from ...constants import LOGO_URL
from telebot import types
from telebot import TeleBot


bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)

@bot.message_handler(commands=[Start.name])
@telegram_user
def start(message: types.Message, user: Telegram):
    bot.send_photo(
        message.chat.id,
        photo=LOGO_URL,
        caption=Start.message,
        reply_markup=Menu.markup(user),
        parse_mode='html'
    )


@bot.message_handler(commands=[Profile.name])
@telegram_user
def profile(message: types.Message, user: Telegram):
    bot.send_photo(
        chat_id=message.chat.id,
        photo=LOGO_URL,
        caption=Profile.message(user),
        reply_markup=Profile.markup(user),
        parse_mode='html'
    )


@bot.message_handler(commands=[Games.name])
def games(message: types.Message):
    bot.send_photo(
        chat_id=message.chat.id,
        photo=LOGO_URL,
        caption=Games.message(),
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
                text=Menu.message(user),
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

        case Games.name:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text=Games.message(),
                parse_mode='html'
            )
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=Games.markup()
            )

        case _:
            if call.data.startswith('game'):
                try:
                    game = Game.objects.get(
                        pk=int(call.data.split(':')[1])
                    )
                except Game.DoesNotExist:
                    return
                
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    text=GameDetailed.message(game),
                    parse_mode='html'
                )
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    reply_markup=GameDetailed.markup(game)
                )
                bot.edit_message_media(
                    media=GameDetailed.media(game),
                    chat_id=call.message.chat.id,
                    message_id=call.message.id
                )
            elif call.data.startswith('edit'):
                pass
            else:
                bot.send_message(
                    chat_id=call.message.chat.id,
                    text=call.data,
                    parse_mode='html'
                )


@telegram_user
def edit_first_name(message: types.Message, user: Telegram):
    user.first_name = message.text
    user.save()
    bot.edit_message_media(
        media='blob:https://web.telegram.org/dd6bb034-a24e-43df-ac73-8caaec60cc06',
        chat_id=message.chat.id,
        message_id=message.id
    )


class Command(BaseCommand):
    help = 'Telegram bot setup command '

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        # bot.polling(non_stop=False)
        bot.infinity_polling()
