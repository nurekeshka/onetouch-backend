from apps.accounts.verification.models import PhoneVerification
from rest_framework.test import APITestCase
from .constants import VerificationSuccessMessages
from .constants import VerificationErrorMessages
from .constants import VerificationRoutes
from rest_framework import status
from django.urls import reverse
from ..constants import CONFIRMED


class CreatePhoneVerificationTest(APITestCase):
    route = VerificationRoutes.create.value

    def test_start_phone_verification_valid(self):
        url = reverse(self.route)

        valid_phone_numbers = (
            '+77003377191',
            '+7 (701) 33-77-191',
            '+7 702 33 77 191',
            '+7703 337-71-91',
            '+7(704)33-77-191)',
            '+7 (705)   33-77   -191',
        )

        for phone in valid_phone_numbers:
            response = self.client.post(url, { 'phone': phone }, format='multipart')
            data = response.json()

            message = data.get('success')
            phone = data.get('data').get('phone')
            code = data.get('data').get('code')

            verification = PhoneVerification.objects.get(phone=phone)
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
            self.assertEqual(VerificationSuccessMessages.send_sms_code.value, message)
            self.assertTrue(code.isdigit(), msg=response.json())
            self.assertEqual(verification.code, code)

    
    def test_start_phone_verification_invalid(self):
        url = reverse(self.route)

        invalid_phone_numbers = (
            'helloworld',
            '22341234212',
            '1',
            '+77003377191*',
            '*87003377191',
        )

        for phone in invalid_phone_numbers:
            response = self.client.post(url, { 'phone': phone }, format='multipart')
            data = response.json()
            message = data.get('error')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(message, VerificationErrorMessages.invalid_phone.value)
            self.assertEqual(PhoneVerification.objects.count(), 0)


class ConfirmVerificationTest(APITestCase):
    route = VerificationRoutes.verify.value

    def test_verify_phone_valid(self):
        url = reverse(self.route)
        phone = '+77003377191'
        code = '1234'

        PhoneVerification.objects.create( phone=phone, code=code ).save()

        data = { 'phone': phone, 'code': code }
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED, msg=response.data)
    

    def test_verify_phone_invalid(self):
        url = reverse(self.route)
        phone = '+77003377191'
        code = '1234'

        data = { 'phone': phone, 'code': code }
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        PhoneVerification.objects.create(phone=phone, code=code)

        data = { 'phone': phone }
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

        verification = PhoneVerification.objects.get()
        verification.code = CONFIRMED
        verification.save()

        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
