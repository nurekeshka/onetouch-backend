from .serializers import GameSerializer, TeamSerializer
from .models import Game, Team


# GETTING GAME FOR APPLICATION FEED
# recieves: date, ordering

def get_games_for_day(date, ordering):
    ordering = 1 if int(ordering) else -1
    
    games = Game.objects.filter(date=date).order_by('start', )[0::ordering]

    answer = list()

    for game in games:
        answer.append({
            'address': game.field.address,
            'field_raiting': game.field.calculate_rate(),
            'latitude': game.field.latitude,
            'longitude': game.field.longitude,
            'players_left': game.players_left(),
            'photo': game.field.photo.link
        })
    
    return answer, 200


# GETTING DETAILED GAME INFORMATION
# recieves: id


def game_detailed(params):
    if params.get('id'):
        return {'id': 'id is not given'}, 400
