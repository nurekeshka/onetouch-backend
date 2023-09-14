from typing import List
from ..fields.models import Photo
from .models import Game


def games_for_day(date: str, ordering: int or None = None):
    games = Game.objects.filter(date=date).order_by('start')
    return games[:: ordering]


def serialize_games(games: List[Game]):
    data = list()

    for game in games:
        data.append(serialize_for_feed(game))

    return data


def serialize_for_feed(game: Game):
    return {
        'id': game.id,
        'address': game.field.address,
        'name': f'Игра дома у Нурбека',
        'start_time': game.start.strftime("%H:%M"),
        'end_time': game.end.strftime("%H:%M"),
        'field_raiting': game.field.calculate_rate(),
        'latitude': game.field.latitude,
        'longitude': game.field.longitude,
        'players_left': game.players_left(),
        'photo': Photo.objects.filter(field=game.field)[0].link
    }
