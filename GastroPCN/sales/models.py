from django.db import models
from catalog.models import Cliente, Revendedor, Producto

class BoletaVenta(models.Model):
    ESTADOS = [('borrador','Borrador'),('emitida','Emitida'),('anulada','Anulada')]
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    revendedor = models.ForeignKey(Revendedor, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='borrador')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_comision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_gas = models.CharField(max_length=20, choices=[('envasado','Envasado'),('natural','Natural')])

    def __str__(self):
        return f"Boleta {self.id} - {self.cliente}"


class DetalleBoleta(models.Model):
    boleta = models.ForeignKey(BoletaVenta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    comision_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"


class ComisionRevendedor(models.Model):
    ESTADOS = [('pendiente','Pendiente'),('pagado','Pagado')]
    revendedor = models.ForeignKey(Revendedor, on_delete=models.CASCADE)
    boleta = models.ForeignKey(BoletaVenta, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.revendedor} - {self.monto} ({self.estado})"
