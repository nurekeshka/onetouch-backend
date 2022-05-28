from .constants import confirmed
from rest_framework import serializers
from rest_framework.authtoken.models import Token
import phonenumbers as pns
from .models import User, Verification


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'photo', 'phone', 'birth_date')   

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        return user

    def validate_phone(self, value):
        ''' Check if phone answers the format '''
        try:
            if pns.is_possible_number(pns.parse(value)):
                pass
        except:
            raise serializers.ValidationError('Phone has wrong format. It should contain: Country Code, National Number')

        ''' Check if phone exists in verification table '''
        if not Verification.objects.filter(phone=value).exists():
            raise serializers.ValidationError('Phone does not exist in verification table')
        
        ''' Check if phone finished verification process '''
        if Verification.objects.get(phone=value).code != confirmed:
            raise serializers.ValidationError('Phone verification process have not finished')

        return value


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'photo', 'phone', 'birth_date', 'date_joined')
    def validate_phone(self, value):
        try:
            if pns.is_possible_number(pns.parse(value)):
                return value
        except:
            raise serializers.ValidationError('Phone has wrong format. It should contain: Country Code, National Number')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)
