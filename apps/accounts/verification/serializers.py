from rest_framework import serializers
from .models import PhoneVerification
from .constants import VerificationErrorMessages


class PhoneVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = ('phone', 'code')

    def validate_phone(self, value: str):
        ''' Check if phone answers the format '''
        if value is None:
            raise serializers.ValidationError(VerificationErrorMessages.none_phone.value)

        if not (~value.find('+') and value[value.find('+') + 1:].isdigit()) or len(value) < 12:
            raise serializers.ValidationError(VerificationErrorMessages.invalid_phone.value)
        
        return value
