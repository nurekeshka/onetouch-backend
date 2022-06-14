from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import utils


@api_view(['POST'])
def start_phone_verification(request):
    phone = request.POST.get('phone')

    if phone is None:
        return Response(data={'error': 'phone is not specified'}, status=400)
    
    body, status = utils.start_new_verification(phone)
    return Response(data=body, status=status)


@api_view(['PUT'])
def verificate_phone(request):
    body, status = utils.verify(request.POST)
    return Response(data=body, status=status)
