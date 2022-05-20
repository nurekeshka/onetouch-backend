from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from rest_framework.decorators import api_view
from django.conf import settings
import requests, urllib.parse
from random import randint
from .models import Profile


COMPLETED = settings.COMPLETED
API_KEY = settings.API_KEY


@api_view(['POST'])
def send_profile_verification(request):
    ''' Отправка СМС сообщения для верификации телефонного номера '''
    phone = request.POST.get('phone')
    code = randint(1000, 9999)


    
    try:
        profile = Profile.objects.get(phone=phone)
        return Response(data='User already exists', status=406)
    except Profile.DoesNotExist:
        pass

    response = requests.get(
        url='https://api.mobizon.kz/service/Message/SendSmsMessage',
        params={
            'apiKey': API_KEY,
            'recipient': urllib.parse.quote(phone),
            'text': urllib.parse.quote(f'Код для верификации номера: {code}')
        }
    )

    if response.json()['code'] == 0:
        profile = Profile.objects.create(phone=phone, verification=code)
        profile.save()

    return Response(response.json(), status=response.status_code)


def _profile_is_verified(profile: Profile) -> bool:
    if profile.verification == COMPLETED:
        return True
    else:
        return False

def _format_phone_number(phone: str) -> str:
    if ~phone.find('+'):
        phone = phone[phone.find('+') + 1:]
    return phone


@api_view(['GET'])
def profile_is_verified(request):
    ''' Проверка завершена-ли верификация '''
    try:
        profile = Profile.objects.get(phone=request.GET.get('phone'))
    except Profile.DoesNotExist:
        return Response(data='Profile with that phone number does not exist', status=406)

    return Response(_profile_is_verified(profile))


@api_view(['GET'])
def verify_profile_phone(request):
    ''' Верификация телефонного номера с проверкой СМС кода '''
    phone = request.GET.get('phone')
    code = request.GET.get('code')

    try:
        profile = Profile.objects.get(phone=phone)
    except Profile.DoesNotExist:
        return Response(data='Profile with that phone number does not exist', status=406)

    if profile.verification != COMPLETED:
        if profile.verification == code:
            profile.verification = COMPLETED
            profile.save()
            return Response(data='Success', status=200)
        else:
            return Response(data='Incorrect verification code', status=406)
    else:
        return Response(data='Profile is verified', status=400)


@api_view(['POST'])
def create_verified_user(request):
    ''' После проверки пользователя заполнение информации '''
    phone = request.POST.get('phone')
    
    try:
        profile = Profile.objects.get(phone=phone)
    except Profile.DoesNotExist:
        return Response(data='Profile with that number does not exist', status=406)

    if profile.verification == COMPLETED:
        if not profile.user:
            user = User.objects.create(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name')
            )

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
        username=request.GET.get('username'),
        password=request.POST.get('password')
    )

    if user is not None:
        login(request, user)
    else:
        return Response(data='Username or password is not valid', status=406)


@api_view(['GET'])
def sign_out(request):
    logout(request)
    return Response(data='Success', status=200)
