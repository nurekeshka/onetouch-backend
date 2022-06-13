from apps.common.games.models import Player
from .models import Telegram
import telebot


def telegram_user(function):
    def inner(payload: telebot.types.Message):
        user, created  = Telegram.objects.get_or_create(
            id=payload.from_user.id,
            defaults={
                'username': payload.from_user.username,
                'first_name': payload.from_user.first_name,
                'last_name': payload.from_user.last_name
            }
        )

        function(payload, user)
    return inner
