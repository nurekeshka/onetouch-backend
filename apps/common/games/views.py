from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import utils


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all(request):
    body, status = utils.get_all_for_day(
        date=request.GET.get('date'),
        ordering=request.GET.get('ordering')
    )
    
    return Response(data=body, status=status)
