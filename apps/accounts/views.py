from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import service


@api_view(['POST'])
def create_user(request):
    body, status = service.create_verified_user(request.POST)
    return Response(data=body, status=status)
