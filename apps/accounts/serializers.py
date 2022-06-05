from rest_framework.authtoken.models import Token
from .verification.models import PhoneVerification
from rest_framework import serializers
from .constants import confirmed
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'photo', 'phone', 'birth_date')   

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        PhoneVerification.objects.get(phone=validated_data.get('phone')).delete()

        return user

    def validate_phone(self, value):
        ''' Check if phone exists in verification table '''
        if not PhoneVerification.objects.filter(phone=value).exists():
            raise serializers.ValidationError('Phone does not exist in verification table')
        
        ''' Check if phone finished verification process '''
        if PhoneVerification.objects.get(phone=value).code != confirmed:
            raise serializers.ValidationError('Phone verification process have not finished')

        return value


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)
