from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from rest_framework.decorators import api_view
from django.conf import settings
import requests, urllib.parse
from random import randint
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer


@api_view(['GET'])
def test(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def send_profile_verification(request):
    ''' Отправка СМС сообщения для верификации телефонного номера '''
    ''' profiles/send-sms-verification '''
    phone = request.POST.get('phone')
    code = randint(1000, 9999)
    
    if Profile.objects.filter(phone=phone).exists():
        return Response(data='Profile already exists', status=406)

    # response = requests.get(
    #     url='https://api.mobizon.kz/service/Message/SendSmsMessage',
    #     params={
    #         'apiKey': settings.API_KEY,
    #         'recipient': urllib.parse.quote(_format_phone_number(request.POST.get('phone'))),
    #         'text': urllib.parse.quote(f'Код для верификации номера: {code}')
    #     }
    # )

    # if response.json()['code'] == 0:
    profile = Profile.objects.create(phone=phone, verification=code)
    profile.save()

    serializer = ProfileSerializer(profile, many=False)

    # return Response(response.json(), status=response.status_code)
    return Response(serializer.data)


@api_view(['GET'])
def verify_profile_phone(request):
    ''' Верификация телефонного номера с проверкой СМС кода '''
    ''' profiles/verify-phone '''
    phone = request.GET.get('phone')
    code = request.GET.get('code')

    if not Profile.objects.filter(phone=phone).exists():
        return Response(data='Profile with that phone number does not exist', status=406)

    profile = Profile.objects.get(phone=phone)

    if profile.verification != settings.COMPLETED:
        if profile.verification == code:
            profile.verification = settings.COMPLETED
            profile.save()
            return Response(data='Success', status=200)
        else:
            return Response(data='Incorrect verification code', status=406)
    else:
        return Response(data='Profile is verified', status=400)


@api_view(['GET'])
def profile_is_verified(request):
    ''' Проверка завершена-ли верификация '''
    ''' profiles/verified '''
    profile = Profile.objects.filter(phone=request.GET.get('phone'))

    if profile.exists():
        return Response(profile[0].is_verified())
    else:
        return Response(data='Profile with that phone number does not exist', status=406)    


@api_view(['POST'])
def create_verified_user(request):
    ''' После проверки пользователя заполнение информации '''
    phone = request.POST.get('phone')
    
    if not Profile.objects.filter(phone=phone).exists():
        return Response(data='Profile with that number does not exist', status=406)

    profile = Profile.objects.get(phone=phone)

    if profile.verification == settings.COMPLETED:
        if not profile.user:
            user = User.objects.create(
                username=request.POST.get('username'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name')
            )

            user.set_password(request.POST.get('password'))
            user.save()

            profile.user = user
            profile.photo = request.POST.get('photo')
            profile.save()

            return Response(data='User created successfully', status=201)
        else:
            return Response(data='User with that profile is already created', status=406)
    else:
        return Response(data='User is not verified', status=406)


@api_view(['POST'])
def sign_in(request):
    user = authenticate(
        request=request,
        username=request.POST.get('username'),
        password=request.POST.get('password')
    )

    if user is not None:
        login(request, user)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    else:
        return Response(data='Username or password is not valid', status=406)


@api_view(['GET'])
def sign_out(request):
    logout(request)
    return Response(data='Success', status=200)


@api_view(['GET'])
def is_authenticated(request):
    return Response(request.user.is_authenticated)


def _format_phone_number(phone: str) -> str:
    if ~phone.find('+'):
        phone = phone[phone.find('+') + 1:]
    return phone
