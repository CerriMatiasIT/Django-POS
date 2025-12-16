#sales/tests/test_reportes_anulados.py
from django.test import TestCase
from django.utils import timezone
from catalog.models import Cliente, Revendedor, Producto
from sales.models import BoletaVenta, DetalleBoleta, ComisionRevendedor

class TestReporteMensualExclusion(TestCase):
    def setUp(self):
        # Cliente y revendedor
        self.cliente = Cliente.objects.create(
            nombre="Cliente Reporte",
            direccion="Av. Rivadavia 2000",
            partido="Morón",
            telefono="777-888"
        )
        self.revendedor = Revendedor.objects.create(
            nombre="Revendedor Reporte",
            contacto="rev@reporte.com",
            estado=True
        )

        # Producto
        self.producto = Producto.objects.create(
            nombre="Cocina Deluxe",
            codigo="REP002",
            tipo_gas="envasado",
            precio_pvp=15000,
            estado=True
        )

        fecha_actual = timezone.now()

        # Boleta emitida
        boleta_emitida = BoletaVenta.objects.create(
            cliente=self.cliente,
            revendedor=self.revendedor,
            estado="emitida",
            total=15000,
            total_comision=1200,
            costo_envio=0,
            tipo_gas="envasado",
            fecha=fecha_actual
        )
        DetalleBoleta.objects.create(
            boleta=boleta_emitida,
            producto=self.producto,
            cantidad=1,
            precio_unitario=15000,
            subtotal=15000,
            comision_item=1200
        )
        ComisionRevendedor.objects.create(
            revendedor=self.revendedor,
            boleta=boleta_emitida,
            monto=1200,
            estado="pendiente"
        )

        # Boleta anulada
        boleta_anulada = BoletaVenta.objects.create(
            cliente=self.cliente,
            revendedor=self.revendedor,
            estado="anulada",
            total=20000,
            total_comision=1500,
            costo_envio=0,
            tipo_gas="envasado",
            fecha=fecha_actual
        )
        DetalleBoleta.objects.create(
            boleta=boleta_anulada,
            producto=self.producto,
            cantidad=2,
            precio_unitario=10000,
            subtotal=20000,
            comision_item=1500
        )
        ComisionRevendedor.objects.create(
            revendedor=self.revendedor,
            boleta=boleta_anulada,
            monto=1500,
            estado="pendiente"
        )

    def test_reporte_mensual_excluye_boletas_anuladas(self):
        fecha_actual = timezone.now()
        boletas_mes = BoletaVenta.objects.filter(
            estado="emitida",
            fecha__year=fecha_actual.year,
            fecha__month=fecha_actual.month
        )

        total_ventas = sum(b.total for b in boletas_mes)
        total_comisiones = sum(b.total_comision for b in boletas_mes)

        # Validaciones: solo debe contar la boleta emitida
        self.assertEqual(total_ventas, 15000, "El total de ventas debe excluir boletas anuladas")
        self.assertEqual(total_comisiones, 1200, "El total de comisiones debe excluir boletas anuladas")
