from .serializers import GameSerializer, FieldSerializer, FeedbackSerializer
from .models import Game, Field, Feedback, Photo
from apps.core.models import User
from faker import Faker


def get_all_games(params):
    ordering = 1 if int(params.get('increment')) else -1
    
    games = Game.objects.filter(date=params['date']).order_by('start', )[0::ordering]
    serializer = GameSerializer(games, many=True)
    
    return serializer.data, 200


def test(data):
    create_fake_fields(15)


def create_fake_users(count: int):
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

def create_fake_fields(count: int):
    fake = Faker()

    for _ in range(count):
        photo = Photo.objects.create(link=fake.url())
        photo.save()

        field = Field.objects.create(
            address=fake.address(),
            photo=photo
        )

        field.save()
