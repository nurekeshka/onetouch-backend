from django.conf import settings
from rest_framework.views import APIView
from .serializers import PhoneVerificationSerializer
from .constants import VerificationSuccessMessages
from .constants import VerificationErrorMessages
from ..constants import AccountsErrorMessages
from .response import SuccessCreatedResponse
from .response import SuccessAcceptedResponse
from .response import BadRequestException
from .response import NotFoundException
from . import utils


class CreatePhoneVerification(APIView):
    def post(self, request, *args, **kwargs):
        phone = utils.format_phone(request.POST.get('phone'))
        recover = bool(request.POST.get('recover'))

        verification_exists = utils.verification_exists(phone)
        account_exists = utils.account_exists(phone)

        if not recover and account_exists:
            return BadRequestException(AccountsErrorMessages.exists.value)

        if recover and not account_exists:
            return NotFoundException(AccountsErrorMessages.not_exist.value)

        if verification_exists:
            utils.delete_verification(phone)

        serializer = PhoneVerificationSerializer(data={ 'phone': phone, 'code': utils.create_random_code() }, many=False)
        
        if not serializer.is_valid():
            return BadRequestException(serializer.errors['phone'][0])
        
        verification = serializer.create(serializer.validated_data)

        if settings.ENABLE_SMS:
            data = utils.send_confirmation_code(verification.phone, verification.code)

            if data.get('code') is not 0:
                return BadRequestException(message=data.get('message'), data=data)
        
        return SuccessCreatedResponse(message=VerificationSuccessMessages.send_sms_code.value, data=serializer.data)


class ConfirmVerification(APIView):
    def put(self, request, *args, **kwargs):
        phone = request.POST.get('phone')
        code = request.POST.get('code')

        if not utils.verification_exists(phone):
            return NotFoundException(message=VerificationErrorMessages.not_exist_phone.value)
        
        verification = utils.get_phone_verification(phone)

        if verification.confirm(code):
            return SuccessAcceptedResponse(message=VerificationSuccessMessages.verified.value)
        
        return BadRequestException(message=VerificationErrorMessages.invalid_code.value)
