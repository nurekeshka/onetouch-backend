from apps.accounts.verification.models import PhoneVerification
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from faker import Faker

from apps.accounts.verification.serializers import PhoneVerificationSerializer


class VerificationTest(APITestCase):
    def test_start_phone_verification_valid(self):
        url = reverse('start-phone-verification')

        valid_phone_numbers = (
            '+77003377191',
            '+7 (701) 33-77-191',
            '+7 702 33 77 191',
            '+7703 337-71-91',
            '+7(704)33-77-191)',
            '+7 (705)   33-77   -191',
        )

        for phone in valid_phone_numbers:

            data = { 'phone': phone }
            response = self.client.post(url, data, format='multipart')
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=self._message(phone, response.json()))
            self.assertEqual(PhoneVerification.objects.count(), 1, msg=self._message(phone, response.json()))
            self.assertTrue(PhoneVerification.objects.get().code.isdigit(), msg=self._message(phone, response.json()))
            PhoneVerification.objects.all().delete()

    
    def test_start_phone_verification_invalid(self):
        url = reverse('start-phone-verification')

        invalid_phone_numbers = (
            'helloworld',
            '22341234212',
            '1',
            '+77003377191*',
            '*87003377191'
        )

        for phone in invalid_phone_numbers:
            data = { 'phone': phone }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=self._message(phone, response.json()))
            self.assertEqual(PhoneVerification.objects.count(), 0, msg=self._message(phone, response.json()))
        

    def test_verify_phone_valid(self):
        url = reverse('verify-phone')
        phone = '+77003377191'
        code = '1234'

        PhoneVerification.objects.create(
            phone=phone, code=code
        ).save()

        data = { 'phone': phone, 'code': code }
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=self._message(phone, response.json()))
        self.assertEqual(PhoneVerification.objects.count(), 0, msg=self._message(phone, response.json()))


    def _message(phone: str, json: dict) -> str:
        return f'\n\nTesting phone number:\t{phone}. \nRecieved: \n\t{json}'
