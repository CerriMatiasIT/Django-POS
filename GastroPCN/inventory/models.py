from django.db import models
from catalog.models import Producto

class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    stock_actual = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.producto} - Stock: {self.stock_actual}"


class MovimientoInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('entrada','Entrada'),('salida','Salida')])
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    referencia = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tipo} {self.cantidad} de {self.producto}"
