from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import service


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_games(request):
    body, status = service.games_for_one_day(request.GET)
    return Response(data=body, status=status)


@api_view(['GET'])
def test(request):
    response = service.test(request.GET)
    return Response(data=response)