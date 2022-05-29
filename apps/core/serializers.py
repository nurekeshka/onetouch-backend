from rest_framework.authtoken.models import Token
from .models import User, Verification
from rest_framework import serializers
from .constants import confirmed
import phonenumbers as pns


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'photo', 'phone', 'birth_date')   

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        Verification.objects.get(phone=validated_data.get('phone')).delete()

        return user

    def validate_phone(self, value):
        ''' Check if phone exists in verification table '''
        if not Verification.objects.filter(phone=value).exists():
            raise serializers.ValidationError('Phone does not exist in verification table')
        
        ''' Check if phone finished verification process '''
        if Verification.objects.get(phone=value).code != confirmed:
            raise serializers.ValidationError('Phone verification process have not finished')

        return value


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ('phone', 'code')

    def create(self, validated_data):
        return Verification.objects.create(**validated_data)

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
