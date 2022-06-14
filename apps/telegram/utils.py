from apps.common.games.models import Player, Team
from .models import Telegram
import telebot


def telegram_user(function):
    def inner(message: telebot.types.Message):
        user, created = Telegram.objects.get_or_create(
            id=message.from_user.id,
            defaults={
                'username': message.from_user.username,
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name
            }
        )

        function(message, user)
    return inner


def telegram_active_only(bot: telebot.TeleBot):
    def decorator(function):
        def inner(message: telebot.types.Message, user: Telegram):
            if user.is_active():
                function(message, user)
            else:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'Команда: "{message.text}", доступна только для пользователей с заполненным профилем',
                    parse_mode='html'
                )

        return inner
    return decorator


def sign_player_to_game(team: Team, user: Telegram) -> bool:
    try:
        player = Player.objects.get(telegram=user)
    except Player.DoesNotExist:
        return False

    team.players.add(player)
    team.save()

    return True
