from django.db import models

class Upload(models.Model):
    usuario = models.CharField(max_length=100)
    fecha = models.DateField()
    laboratorio = models.CharField(max_length=100)
    cuit = models.CharField(max_length=11)
    file = models.JSONField()  # Cambiar el tipo de campo a JSONField para almacenar el DataFrame
    uploaded_at = models.DateTimeField(auto_now_add=True)
