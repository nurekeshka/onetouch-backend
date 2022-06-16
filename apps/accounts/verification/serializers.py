from apps.accounts.models import User
from rest_framework import serializers
from .models import PhoneVerification
import phonenumbers as pns


class PhoneVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = ('phone', 'code')

    def create(self, validated_data):
        return PhoneVerification.objects.create(**validated_data)

    def validate_phone(self, value: str):
        ''' Check if phone answers the format '''
        value = value.strip().replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        
        if not ~value.find('+') and not value[value.find('+') + 1:].isnumeric():
            raise serializers.ValidationError('Phone has wrong format. It should contain: Country Code, National Number')
        
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('User with that phone number already exists')
        
        return value
