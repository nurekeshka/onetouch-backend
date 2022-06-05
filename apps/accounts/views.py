from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import service


@api_view(['POST'])
def verification_sms(request):
    phone = request.POST.get('phone')

    if phone is None:
        return Response(data={'error': 'phone is not specified'}, status=400)
    
    body, status = service.start_new_verification(phone)
    return Response(data=body, status=status)


@api_view(['PUT'])
def verificate_phone(request):
    body, status = service.verify(request.POST)
    return Response(data=body, status=status)


@api_view(['POST'])
def create_user(request):
    body, status = service.create_verified_user(request.POST)
    return Response(data=body, status=status)
