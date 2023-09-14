from apps.accounts.verification.constants import VerificationRoutes
from apps.accounts.verification.models import PhoneVerification
from rest_framework.test import APITestCase
from rest_framework import status
from .constants import AccountsErrorMessages, AccountsRoutes
from .constants import CONFIRMED
from apps.accounts.models import User
from django.urls import reverse


class AccountsTest(APITestCase):
    route = AccountsRoutes.sign_up.value
    verification_route = VerificationRoutes.create.value

    def test_create_user_valid(self):
        url = reverse(self.route)
        phone = '+77003377191'

        PhoneVerification.objects.create( phone=phone, code=CONFIRMED )

        data = {
            'phone': phone,
            'username': 'username',
            'password': 'qwerty12345',
            'first_name': 'nurbek',
            'last_name': 'bolat',
            'email': 'email@example.com',
            'photo': 'https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png',
            'birth_date': '2004-05-12'
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(phone=phone).exists())
        self.assertEqual(PhoneVerification.objects.count(), 0)


    def test_create_user_invalid(self):
        url = reverse(self.route)
        phone = '+77003377191'

        data = {
            'phone': phone,
            'username': 'username',
            'password': 'qwerty12345',
            'first_name': 'nurbek',
            'last_name': 'bolat',
            'email': 'email@example.com',
            'photo': 'https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png',
            'birth_date': '2004-05-12'
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
        self.assertEqual(User.objects.count(), 0, msg=response.data)

        self.client.post(reverse(self.verification_route), data, format='multipart')

        response = self.client.post(reverse(self.route), data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
        self.assertEqual(response.json().get('error'), AccountsErrorMessages.invalid_info.value)
        self.assertEqual(User.objects.count(), 0, msg=response.data)
