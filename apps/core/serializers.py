from rest_framework import serializers
from rest_framework.authtoken.models import Token
import phonenumbers as pns
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'photo', 'phone', 'birth_date')
    def validate_phone(self, value):
        try:
            if pns.is_possible_number(pns.parse(value)):
                pass
        except:
            raise serializers.ValidationError('Phone has wrong format. It should contain: Country Code, National Number')
        
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        return user


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)
