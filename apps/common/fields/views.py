from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .constants import FieldsErrorMessages
from .serializers import PhotoSerializer
from .serializers import FieldSerializer
from .response import BadRequestException
from .response import NotFoundException
from . import utils


class GeocodeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        address = request.GET.get('address')
        response = utils.get_lat_and_long(address)

        return Response(data=response.json(), status=response.status_code)


class PhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        field_id = int(request.GET.get('field-id'))
        field = utils.get_field_by_id(field_id)

        photos = utils.get_all_photos(field)

        serializer = PhotoSerializer(instance=photos, many=True)
        return Response(data=serializer.data)


class FieldView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            id = int(request.GET.get('id'))
        except (ValueError, TypeError):
            return BadRequestException(FieldsErrorMessages.bad_request.value)
        else:
            if not utils.field_exists(id):
                return NotFoundException(FieldsErrorMessages.not_found.value)

        field = utils.get_field_by_id(id)

        serializer = FieldSerializer(instance=field, many=False)
        return Response(data=serializer.data)
