from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Más adelante: roles, auditoría, etc.
    pass

class Auditoria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    detalle = models.TextField()

    def __str__(self):
        return f"{self.usuario} - {self.accion} ({self.fecha})"
