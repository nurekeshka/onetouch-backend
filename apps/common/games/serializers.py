from rest_framework import serializers
from .models import Game, Team


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'field', 'form', 'date', 'start', 'end', 'payment')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'players', 'game')
