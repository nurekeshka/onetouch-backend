from rest_framework import serializers
from .models import Field, Feedback
from .models import Photo


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('id', 'address', 'latitude', 'longitude', 'contacts')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'raiting', 'description', 'user', 'field')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'link')
