from apps.accounts.models import User
from rest_framework import serializers
from .models import PhoneVerification


class PhoneVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = ('phone', 'code')

    def create(self, validated_data):
        return PhoneVerification.objects.create(**validated_data)

    def validate_phone(self, value: str):
        ''' Check if phone answers the format '''
        if not (~value.find('+') and value[value.find('+') + 1:].isdigit()) or len(value) < 12:
            raise serializers.ValidationError('Формат телефонного номера не правильный. Он должен содержать: код страны, национальный номер и быть длинной в 12 символов')
        
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('Пользователь с таким телефонным номером уже существует')
        
        return value
