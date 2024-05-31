# tasks/serializers.py
from rest_framework import serializers
from .models import Task, Taskes

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taskes
        fields = '__all__'
