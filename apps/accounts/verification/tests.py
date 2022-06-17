from apps.accounts.verification.models import PhoneVerification
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from faker import Faker


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
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=f'\n\nTesting phone number:\t{phone}. \nRecieved: \n\t{response.json()}')
            self.assertEqual(PhoneVerification.objects.count(), 1)
            self.assertTrue(PhoneVerification.objects.get().code.isdigit())
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
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(PhoneVerification.objects.count(), 0)

