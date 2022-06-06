from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import utils


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_fake_information(request):
    if request.user.is_staff:
        utils.create_fake_information()


@api_view(['GET'])
def get_latitude_and_longitude(request):
    response = utils.get_lat_and_long(request.GET.get('address'))
    return Response(data=response)
