from django.shortcuts import render
from rest_framework import viewsets
from .models import Task,Taskes
from .serializer import TaskSerializer

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer