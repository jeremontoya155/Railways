from rest_framework import serializers
from .models import Task,Taskes


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=(Task,Taskes)
        
        fields='__all__' 