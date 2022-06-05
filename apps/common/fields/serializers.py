from rest_framework import serializers
from .models import Field, Feedback


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('id', 'address', 'latitude', 'longitude', 'photo', 'contacts')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'raiting', 'description', 'user', 'field')
