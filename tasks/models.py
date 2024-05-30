from django.db import models

# Create your models here.
class Task(models.Model):
    title=models.CharField(max_length=200)
    completed=models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


class Taskes(models.Model):
    title=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    surname=models.CharField(max_length=200)
    descripcion=models.CharField(max_length=200)
    completed=models.BooleanField(default=False)
    
    def __str__(self):
        datos = (
            f'Título: {self.title}\n'
            f'Nombre: {self.name}\n'
            f'Apellido: {self.surname}\n'
            f'Descripción: {self.descripcion}'
        )
        return datos