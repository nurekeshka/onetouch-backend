from apps.accounts.verification.models import PhoneVerification
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class VerificationTest(APITestCase):
    def test_start_phone_verification_valid(self):
        url = reverse('start-phone-verification')
        data = { 'phone': '+77003377191' }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PhoneVerification.objects.count(), 1)
        self.assertTrue(PhoneVerification.objects.get().code.isdigit())

    
    def test_start_phone_verification_invalid(self):
        url = reverse('start-phone-verification')

        invalid_phone_numbers = [
            'helloworld',
            '22341234212',
            '1',
        ]

        for phone in invalid_phone_numbers:
            data = { 'phone': phone }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(PhoneVerification.objects.count(), 0)

