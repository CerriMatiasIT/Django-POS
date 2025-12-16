from django.db import models
from catalog.models import Proveedor, Producto
from django.conf import settings
from inventory.models import Inventario, MovimientoInventario

class CompraEntrada(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True, null=True)
    creada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Entrada {self.id} - {self.proveedor}"
    
    def confirmar(self, usuario=None):
        """
        Confirma la entrada:
        - Incrementa stock en Inventario.
        - Registra MovimientoInventario.
        - Calcula total de la entrada.
        """
        total = 0
        for detalle in self.detalles.all():
            # Actualizar stock
            inv, _ = Inventario.objects.get_or_create(producto=detalle.producto)
            inv.stock_actual += detalle.cantidad
            inv.save()

            # Registrar movimiento
            MovimientoInventario.objects.create(
                producto=detalle.producto,
                tipo="entrada",
                cantidad=detalle.cantidad,
                referencia=f"Entrada {self.id}"
            )

            total += detalle.costo_unitario * detalle.cantidad

        self.total = total
        self.save()


class DetalleEntrada(models.Model):
    entrada = models.ForeignKey(CompraEntrada, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
