# sales/tests/test_total_boleta.py
from django.test import TestCase
from catalog.models import Cliente, Revendedor, Producto, TarifaEnvio
from sales.models import BoletaVenta, DetalleBoleta

class TestTotalBoletaConEnvio(TestCase):
    def setUp(self):
        # Cliente y revendedor
        self.cliente = Cliente.objects.create(
            nombre="Cliente Total",
            direccion="Calle Belgrano 456",
            partido="Morón",
            telefono="123-456"
        )
        self.revendedor = Revendedor.objects.create(
            nombre="Revendedor Total",
            contacto="rev@total.com",
            estado=True
        )

        # Producto
        self.producto = Producto.objects.create(
            nombre="Cocina Básica",
            codigo="TOT001",
            tipo_gas="envasado",
            precio_pvp=10000,
            estado=True
        )

        # Tarifa de envío para Morón
        self.tarifa = TarifaEnvio.objects.create(
            localidad="Morón",
            precio_sugerido=800,
            fletero="Fletero Morón"
        )

        # Boleta en borrador
        self.boleta = BoletaVenta.objects.create(
            cliente=self.cliente,
            revendedor=self.revendedor,
            estado="borrador",
            tipo_gas="envasado"
        )

        # Detalle de boleta
        DetalleBoleta.objects.create(
            boleta=self.boleta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=10000,
            subtotal=20000,
            comision_item=1500
        )

    def test_calculo_total_incluye_envio(self):
        # Asignar costo de envío según localidad del cliente
        tarifa = TarifaEnvio.objects.filter(localidad=self.cliente.partido).first()
        if tarifa:
            self.boleta.costo_envio = tarifa.precio_sugerido

        # Calcular total: productos + envío
        total_productos = sum(d.subtotal for d in self.boleta.detalles.all())
        self.boleta.total = total_productos + self.boleta.costo_envio
        self.boleta.save()

        # Validaciones
        self.boleta.refresh_from_db()
        self.assertEqual(total_productos, 20000, "El subtotal de productos debe ser correcto")
        self.assertEqual(self.boleta.costo_envio, 800, "El costo de envío debe asignarse según la localidad")
        self.assertEqual(self.boleta.total, 20800, "El total debe incluir productos + envío")
