# sales/tests/test_tarifa_envio.py
from django.test import TestCase
from catalog.models import Cliente, Revendedor, Producto, TarifaEnvio
from sales.models import BoletaVenta, DetalleBoleta

class TestTarifaEnvio(TestCase):
    def setUp(self):
        # Cliente en localidad con tarifa definida
        self.cliente = Cliente.objects.create(
            nombre="Cliente Envío",
            direccion="Calle San Martín 123",
            partido="Morón",
            telefono="999-888"
        )
        self.revendedor = Revendedor.objects.create(
            nombre="Revendedor Envío",
            contacto="rev@envio.com",
            estado=True
        )

        # Producto
        self.producto = Producto.objects.create(
            nombre="Cocina Económica",
            codigo="ENV001",
            tipo_gas="envasado",
            precio_pvp=7000,
            estado=True
        )

        # Tarifa de envío para Morón
        self.tarifa = TarifaEnvio.objects.create(
            localidad="Morón",
            precio_sugerido=500,
            fletero="Fletero Local"
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
            cantidad=1,
            precio_unitario=7000,
            subtotal=7000,
            comision_item=500
        )

    def test_tarifa_envio_asignada_por_localidad(self):
        # Asignar tarifa de envío según localidad del cliente
        tarifa = TarifaEnvio.objects.filter(localidad=self.cliente.partido).first()
        if tarifa:
            self.boleta.costo_envio = tarifa.precio_sugerido
            self.boleta.save()

        # Validaciones
        self.boleta.refresh_from_db()
        self.assertEqual(self.boleta.costo_envio, 500, "El costo de envío debe asignarse según la localidad del cliente")
        self.assertEqual(self.boleta.total, 0, "El total aún no se calcula hasta emitir la boleta")
