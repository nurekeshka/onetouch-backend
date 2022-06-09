from apps.accounts.verification.serializers import PhoneVerificationSerializer
from django.core.management.base import BaseCommand
from telebot import types
from telebot import TeleBot
from django.conf import settings
from ... import constants as const
from ...models import Telegram
from ...utils import telegram_user


bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)

@bot.message_handler(commands=[const.Commands.start])
@telegram_user
def start(message: types.Message, user: Telegram):
    inline = types.InlineKeyboardMarkup()

    if not user.is_active():
        inline.add(
            types.InlineKeyboardButton(
                text=const.ButtonTexts.update,
                callback_data=const.Commands.update
            )
        )
    else:
        inline.add(
            types.InlineKeyboardButton(
                text=const.ButtonTexts.profile,
                callback_data=const.Commands.profile
            ),
            types.InlineKeyboardButton(
                text=const.ButtonTexts.games,
                callback_data=const.Commands.games
            )
        )

    bot.send_message(
        chat_id=message.chat.id, 
        text=const.Messages.start,
        reply_markup=inline,
        parse_mode='html'
    )


@bot.callback_query_handler(func=lambda call: True)
@telegram_user
def query_callback(call: types.CallbackQuery, user: Telegram):
    match call.data:
        case const.Commands.update:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)

            keyboard.add(
                types.KeyboardButton(text='Возраст'),
                types.KeyboardButton(text='Номер телефона')
            )

            msg = bot.send_message(
                chat_id=call.message.chat.id,
                text='Введите информацию',
                reply_markup=keyboard
            )

            bot.register_next_step_handler(
                message=msg,
                callback=update_info
            )


@telegram_user
def update_info(message: types.Message, user: Telegram):
    if message.text == 'Возраст':
        msg = bot.send_message(
            chat_id=message.chat.id,
            text='Введите возраст'
        )

        bot.register_next_step_handler(
            message=msg,
            callback=enter_age
        )
    elif message.text == 'Номер телефона':
        msg = bot.send_message(
            chat_id=message.chat.id,
            text='Введите номер телефона'
        )

        bot.register_next_step_handler(
            message=msg,
            callback=enter_phone_number
        )


@telegram_user
def enter_age(message: types.Message, user: Telegram):
    if message.text.isdigit():
        user.age = int(message.text)
        user.save()
        bot.send_message(
            chat_id=message.chat.id,
            text='Сохранено!'
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='Введите целое число'
        )


@telegram_user
def enter_phone_number(message: types.Message, user: Telegram):
    if PhoneVerificationSerializer().validate_phone(message.text):
        user.phone = message.text
        user.save()

        bot.send_message(
            chat_id=message.chat.id,
            text='Сохранено'
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='Не корректный номер телефона'
        )


class Command(BaseCommand):
    help = 'Telegram bot setup command '

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        print('Telegram BOT has been started')
        # bot.infinity_polling()
        bot.polling(none_stop=False, interval=0)
