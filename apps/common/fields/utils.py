from .models import Field, Feedback, Photo
from apps.accounts.models import User
from django.conf import settings
from faker import Faker
from random import randint
from requests import get


def get_lat_and_long(address: str):
    response = get(
        url='https://graphhopper.com/api/1/geocode/',
        params={
            'q': address,
            'locale': 'ru',
            'limit': 3,
            'key': settings.GEOCODER_API_KEY
        }
    )

    return response.json(), response.status_code


# CREATING FAKE INFORMATION FOR TESTING

def create_fake_information():
    _create_fake_users(50)
    _create_fake_fields(15)

    for field in Field.objects.all():
        _create_fake_feedback(10, field)

    return {'success': True}


def _create_fake_users(count: int):
    fake = Faker()

    for _ in range(count):
        user = User.objects.create(
            phone=fake.phone_number(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birth_date=fake.date(),
            email=fake.email(),
        )

        user.set_password(fake.password())
        user.save()

def _create_fake_fields(count: int):
    fake = Faker()

    for _ in range(count):
        photo = Photo.objects.create(link=fake.url())
        photo.save()

        field = Field.objects.create(
            address=fake.address(),
            photo=photo
        )

        field.save()

def _create_fake_feedback(count: int, field: Field):
    fake = Faker()
    users = User.objects.all()

    for _ in range(count):
        feedback = Feedback.objects.create(
            raiting=randint(0, 10),
            description=fake.text(),
            field=field,
            user=users[randint(0, len(users) - 1)]
        )

        feedback.save()
