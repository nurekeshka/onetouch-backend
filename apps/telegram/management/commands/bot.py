from django.core.management.base import BaseCommand
from django.conf import settings
import telebot


bot = telebot.TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


@bot.message_handler(content_types=['text'])
def echo(message):
    print(message.from_user)
    bot.send_message(message.chat.id, message.text)


class Command(BaseCommand):
    help = 'Telegram bot setup command '

    def handle(self, *args, **kwargs):
        print('Telegram bot started')
        bot.infinity_polling()
