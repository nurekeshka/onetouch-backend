from requests import Response
from requests import get
from typing import List
from django.conf import settings
from .constants import GEOCODER_API_URL
from .models import Photo
from .models import Field


def get_lat_and_long(address: str, limit: int = 3) -> Response:
    return get(
        url=GEOCODER_API_URL,
        params={
            'q': address,
            'locale': 'ru',
            'limit': limit,
            'key': settings.GEOCODER_API_KEY
        }
    )


def get_all_photos(field: Field) -> List[Photo]:
    return Photo.objects.filter(field=field).all()


def get_field_by_id(id: int) -> Field:
    return Field.objects.get(id=id)


def field_exists(id: int) -> bool:
    return Field.objects.filter(id=id).exists()
