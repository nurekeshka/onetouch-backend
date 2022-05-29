from .serializers import GameSerializer
from .models import Game


def get_all_games(params):
    ordering = 1 if int(params.get('increment')) else -1
    
    games = Game.objects.filter(date=params['date']).order_by('start', )[0::ordering]
    serializer = GameSerializer(games, many=True)
    
    return serializer.data, 200
