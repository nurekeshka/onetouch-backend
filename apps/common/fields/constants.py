from enum import Enum


class FieldsRoutes(Enum):
    get_field_by_id = 'field-by-id'
    latitude_longitude = 'latitude-longitude'
    photos = 'field-photos'


class FieldsErrorMessages(Enum):
    not_found = 'поля с таким id не существует'
    bad_request = 'id поля указан неправильно'


GEOCODER_API_URL = 'https://graphhopper.com/api/1/geocode/'
