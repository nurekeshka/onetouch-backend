from apps.accounts.verification.serializers import PhoneVerificationSerializer
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import Telegram
from ...utils import telegram_user
from ...constants import *
from telebot import types
from telebot import TeleBot


bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)

@bot.message_handler(commands=[Start.name])
@telegram_user
def start(message: types.Message, user: Telegram):
    inline = types.InlineKeyboardMarkup()

    if user.is_active():
        inline.add( Profile.button )
    else:
        inline.add()
    
    bot.send_message(
        chat_id=message.chat.id, 
        text=Start.message,
        reply_markup=inline,
        parse_mode='html'
    )


class Command(BaseCommand):
    help = 'Telegram bot setup command '

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.polling(none_stop=False, interval=0)
        # bot.infinity_polling()
