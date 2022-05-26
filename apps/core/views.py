from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import service


@api_view(['GET'])
def verification_sms(request):
    phone = request.GET.get('phone')

    if phone is None:
        return Response(data={'error': 'phone is not specified'}, status=400)
    
    body, code = service.start_new_verification(phone)

    return Response(data=body, status=code)
