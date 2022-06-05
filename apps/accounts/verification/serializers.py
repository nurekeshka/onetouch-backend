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

    def validate_phone(self, value):
        ''' Check if phone answers the format '''
        try:
            if pns.is_possible_number(pns.parse(value)):
                pass
        except:
            raise serializers.ValidationError('Phone has wrong format. It should contain: Country Code, National Number')
        
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('User with that phone number already exists')
        
        return value
