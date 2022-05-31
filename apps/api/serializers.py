from rest_framework import serializers
from .models import Game, Field, Feedback


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'field', 'form', 'date', 'start', 'end', 'signed_users')


class GameFeedSerializer(serializers.Serializer):
    address = serializers.CharField()
    field_raiting = serializers.FloatField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    players_left = serializers.IntegerField()
    photo = serializers.URLField()


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('id', 'address', 'latitude', 'longitude', 'photo', 'contacts')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'raiting', 'description', 'user', 'field')
