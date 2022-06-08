from django.core.management.base import BaseCommand
from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot import TeleBot
from django.conf import settings
from ... import constants as const
from ...models import Telegram
from ...utils import telegram_user
import telebot


bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


@bot.message_handler(commands=[const.Commands.start])
@telegram_user
def start(message, user):
    inline = InlineKeyboardMarkup()

    if not user.is_active():
        inline.add(
            InlineKeyboardButton(
                text=const.ButtonTexts.update,
                callback_data=const.Commands.update
            )
        )
    else:
        inline.add(
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
        reply_markup=inline,
        parse_mode='html'
    )


@bot.callback_query_handler(func=lambda call: True)
@telegram_user
def query_callback(call: telebot.types.CallbackQuery, user: Telegram):
    match call.data:
        case const.Commands.update:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)

            keyboard.add(
                KeyboardButton(text='Возраст'),
                KeyboardButton(text='Номер телефона')
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
def update_info(message: telebot.types.Message, user: Telegram):
    if message.text == 'Возраст':
        print('Возраст')
    elif message.text == 'Номер телефона':
        print('Телефон')


class Command(BaseCommand):
    help = 'Telegram bot setup command '

    def handle(self, *args, **kwargs):
        print('Telegram bot started')
        # bot.infinity_polling()
        bot.polling(none_stop=False, interval=0)
