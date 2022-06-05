from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import service


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all(request):
    body, status = service.games_for_one_day(
        date=request.GET.get('date'),
        ordering=request.GET.get('ordering')
    )
    
    return Response(data=body, status=status)
