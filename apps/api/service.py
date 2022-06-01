from .serializers import GameSerializer, FieldSerializer, FeedbackSerializer, TeamSerializer
from .models import Game, Field, Feedback, Photo
from apps.core.models import User
from faker import Faker
from random import randint


# GETTING GAME FOR APPLICATION FEED
# recieves: date, ordering

def all_games_for_one_day(params):
    ordering = 1 if int(params.get('ordering')) else -1
    
    games = Game.objects.filter(date=params['date']).order_by('start', )[0::ordering]

    answer = list()

    for game in games:
        answer.append({
            'address': game.field.address,
            'field_raiting': game.field.calculate_rate(),
            'latitude': game.field.latitude,
            'longitude': game.field.longitude,
            'players_left': game.players_left(),
            'photo': game.field.photo.link
        })
    
    return answer, 200


# FUNCTIONS FOR TESTING

def test(data):
    game = Game.objects.all()[0]
    return TeamSerializer(game.players_left(), many=True).data


# CREATING FAKE INFORMATION FOR TESTING

def create_fake_information():
    create_fake_users(50)
    create_fake_fields(15)

    fields = Field.objects.all()

    for field in fields:
        create_fake_feedback(10, field)


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


def create_fake_feedback(count: int, field: Field):
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
