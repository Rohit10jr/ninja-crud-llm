from rest_framework import serializers
from .models import Car


class TextSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=100)


class CarSerializer(serializers.Serializer):
    model = Car
    fields = "__all__"
