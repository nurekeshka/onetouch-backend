from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .verification.constants import VerificationErrorMessages
from .verification.models import PhoneVerification
from .constants import CONFIRMED
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'photo', 'phone', 'birth_date')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        PhoneVerification.objects.get(
            phone=validated_data.get('phone')).delete()

        return user

    def validate_phone(self, value):
        ''' Check if phone exists in verification table '''
        if not PhoneVerification.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                VerificationErrorMessages.not_exist_phone.value)

        ''' Check if phone finished verification process '''
        if PhoneVerification.objects.get(phone=value).code != CONFIRMED:
            raise serializers.ValidationError(
                VerificationErrorMessages.not_verified.value)

        return value


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)
