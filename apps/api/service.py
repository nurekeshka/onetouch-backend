from .serializers import GameSerializer, FieldSerializer, FeedbackSerializer
from .models import Game, Field, Feedback


def get_all_games(params):
    ordering = 1 if int(params.get('increment')) else -1
    
    games = Game.objects.filter(date=params['date']).order_by('start', )[0::ordering]
    serializer = GameSerializer(games, many=True)
    
    return serializer.data, 200


def test(data):
    # field = Field.objects.get(id=1)
    # return field.calculate_rate()

    game = Game.objects.get(id=3)
    serializer = GameSerializer(game, many=False)

    return game.players_left()