from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    tipo_gas = models.CharField(max_length=20, choices=[('envasado','Envasado'),('natural','Natural')])
    precio_pvp = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    partido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


class Revendedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class TarifaEnvio(models.Model):
    localidad = models.CharField(max_length=100)
    precio_sugerido = models.DecimalField(max_digits=10, decimal_places=2)
    fletero = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.localidad} - {self.precio_sugerido}"
