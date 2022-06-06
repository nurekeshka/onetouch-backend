from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import utils


@api_view(['POST'])
def create_user(request):
    body, status = utils.create_verified_user(request.POST)
    return Response(data=body, status=status)
