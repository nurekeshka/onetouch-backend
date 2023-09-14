from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import utils


class GamesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        date = request.GET.get('date')
        ordering = 1 if bool(request.GET.get('ordering')) else -1

        games = utils.games_for_day(date, ordering)
        data = utils.serialize_games(games)

        return Response(data, 200)
