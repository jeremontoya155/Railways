# tasks/serializers.py
from rest_framework import serializers
from .models import Upload

class Upload(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'

