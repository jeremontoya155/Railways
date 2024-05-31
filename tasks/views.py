# tasks/views.py
from rest_framework import viewsets
from .models import Task, Taskes
from .serializer import TaskSerializer, TaskesSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskesViewSet(viewsets.ModelViewSet):
    queryset = Taskes.objects.all()
    serializer_class = TaskesSerializer
