from django.core.management.base import BaseCommand
from ... import constants as text
from django.conf import settings
import telebot


bot = telebot.TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


@bot.message_handler(['start'])
def echo(message):
    bot.send_message(message.chat.id, text.START_MESSAGE)


class Command(BaseCommand):
    help = 'Telegram bot setup command '

    def handle(self, *args, **kwargs):
        print('Telegram bot started')
        bot.infinity_polling()
