from dataclasses import fields
from rest_framework import serializers
from .models import Game, Field, Feedback, Team


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'field', 'form', 'date', 'start', 'end', 'signed_users')


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('id', 'address', 'latitude', 'longitude', 'photo', 'contacts')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'raiting', 'description', 'user', 'field')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'players', 'game')
