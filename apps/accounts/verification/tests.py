from apps.accounts.verification.models import PhoneVerification
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class VerificationTest(APITestCase):
    def test_start_phone_verification(self):
        url = reverse('start-phone-verification')
        phone_string = '+77003377191'
        data = { 'phone': phone_string }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PhoneVerification.objects.count(), 1)
        self.assertTrue(PhoneVerification.objects.get().code.isdigit())
