from ...utils import telegram_user, telegram_active_only
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import Telegram
from ...interface import *
from ...constants import LOGO_URL
from telebot import types
from telebot import TeleBot
import phonenumbers as pns


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
@telegram_user
@telegram_active_only(bot)
def games(message: types.Message, user):
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
            bot.edit_message_media(
                media=types.InputMediaPhoto(
                    media=LOGO_URL,
                    caption=Menu.message(user),
                    parse_mode='html'
                ),
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=Menu.markup(user)
            )

        case Profile.name:
            bot.edit_message_media(
                media=types.InputMediaPhoto(
                    media=LOGO_URL,
                    caption=Profile.message(user),
                    parse_mode='html'
                ),
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=Profile.markup(user)
            )

        case Games.name:
            bot.edit_message_media(
                media=types.InputMediaPhoto(
                    media=LOGO_URL,
                    caption=Games.message(),
                    parse_mode='html'
                ),
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
                
                bot.edit_message_media(
                    media=types.InputMediaPhoto(
                        media=GameDetailed.media(game),
                        caption=GameDetailed.message(game),
                        parse_mode='html'
                    ),
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    reply_markup=GameDetailed.markup(game)
                )
            elif call.data.startswith('edit'):
                match call.data.split(':')[1]:
                    case 'first_name':
                        bot.register_next_step_handler(
                            message=bot.send_message(
                                chat_id=call.message.chat.id,
                                text=Edit.first_name.message,
                                parse_mode='html'
                            ),
                            callback=edit_first_name
                        )
                    case 'last_name':
                        bot.register_next_step_handler(
                            message=bot.send_message(
                                chat_id=call.message.chat.id,
                                text=Edit.last_name.message,
                                parse_mode='html'
                            ),
                            callback=edit_last_name
                        )
                    case 'age':
                        bot.register_next_step_handler(
                            message=bot.send_message(
                                chat_id=call.message.chat.id,
                                text=Edit.age.message,
                                parse_mode='html'
                            ),
                            callback=edit_age
                        )
                    case 'phone':
                        bot.register_next_step_handler(
                            message=bot.send_message(
                                chat_id=call.message.chat.id,
                                text=Edit.phone.message,
                                parse_mode='html'
                            ),
                            callback=edit_phone
                        )
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

    profile(message)

@telegram_user
def edit_last_name(message: types.Message, user: Telegram):
    user.last_name = message.text
    user.save()

    profile(message)

@telegram_user
def edit_age(message: types.Message, user: Telegram):
    if message.text.isdigit():
        user.age = message.text
        user.save()

        profile(message)
    else:
        bot.register_next_step_handler(
            message=bot.send_message(
                chat_id=message.chat.id,
                text=Edit.age.error
            ),
            callback=edit_age
        )

@telegram_user
def edit_phone(message: types.Message, user: Telegram):
    try:
        if pns.is_possible_number(pns.parse(message.text)):
            user.phone = message.text
            user.save()
            profile(message)
        else:
            raise TypeError()
    except:
        bot.register_next_step_handler(
            message=bot.send_message(
                chat_id=message.chat.id,
                text=Edit.phone.error
            ),
            callback=edit_phone
        )


class Command(BaseCommand):
    help = 'Telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        # bot.polling(non_stop=False)
        bot.infinity_polling()
