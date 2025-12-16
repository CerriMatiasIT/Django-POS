# sales/tests/test_reportes.py
from django.test import TestCase
from django.utils import timezone
from catalog.models import Cliente, Revendedor, Producto
from sales.models import BoletaVenta, DetalleBoleta, ComisionRevendedor

class TestReporteMensual(TestCase):
    def setUp(self):
        # Cliente y revendedor
        self.cliente = Cliente.objects.create(
            nombre="Cliente Reporte",
            direccion="Av. Rivadavia 1000",
            partido="Morón",
            telefono="555-666"
        )
        self.revendedor = Revendedor.objects.create(
            nombre="Revendedor Reporte",
            contacto="rev@reporte.com",
            estado=True
        )

        # Producto
        self.producto = Producto.objects.create(
            nombre="Cocina Premium",
            codigo="REP001",
            tipo_gas="envasado",
            precio_pvp=12000,
            estado=True
        )

        # Crear boletas emitidas en el mes actual
        fecha_actual = timezone.now()

        # Boleta 1
        boleta1 = BoletaVenta.objects.create(
            cliente=self.cliente,
            revendedor=self.revendedor,
            estado="emitida",
            total=24000,
            total_comision=2000,
            costo_envio=0,
            tipo_gas="envasado",
            fecha=fecha_actual
        )
        DetalleBoleta.objects.create(
            boleta=boleta1,
            producto=self.producto,
            cantidad=2,
            precio_unitario=12000,
            subtotal=24000,
            comision_item=2000
        )
        ComisionRevendedor.objects.create(
            revendedor=self.revendedor,
            boleta=boleta1,
            monto=2000,
            estado="pendiente"
        )

        # Boleta 2
        boleta2 = BoletaVenta.objects.create(
            cliente=self.cliente,
            revendedor=self.revendedor,
            estado="emitida",
            total=12000,
            total_comision=1000,
            costo_envio=0,
            tipo_gas="envasado",
            fecha=fecha_actual
        )
        DetalleBoleta.objects.create(
            boleta=boleta2,
            producto=self.producto,
            cantidad=1,
            precio_unitario=12000,
            subtotal=12000,
            comision_item=1000
        )
        ComisionRevendedor.objects.create(
            revendedor=self.revendedor,
            boleta=boleta2,
            monto=1000,
            estado="pendiente"
        )

    def test_reporte_mensual_totales(self):
        # Filtrar boletas emitidas en el mes actual
        fecha_actual = timezone.now()
        boletas_mes = BoletaVenta.objects.filter(
            estado="emitida",
            fecha__year=fecha_actual.year,
            fecha__month=fecha_actual.month
        )

        # Calcular totales
        total_ventas = sum(b.total for b in boletas_mes)
        total_comisiones = sum(b.total_comision for b in boletas_mes)

        # Validaciones
        self.assertEqual(total_ventas, 36000, "El total de ventas del mes debe coincidir con las boletas emitidas")
        self.assertEqual(total_comisiones, 3000, "El total de comisiones del mes debe coincidir con las boletas emitidas")
