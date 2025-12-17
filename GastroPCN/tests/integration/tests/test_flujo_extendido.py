# integration/tests/test_flujo_extendido.py
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from catalog.models import Cliente, Revendedor, Producto, Proveedor
from inventory.models import Inventario, MovimientoInventario
from purchases.models import CompraEntrada, DetalleEntrada
from sales.models import BoletaVenta, DetalleBoleta, ComisionRevendedor

User = get_user_model()

class TestFlujoExtendido(TestCase):
    def setUp(self):
        # Usuario admin
        self.admin = User.objects.create_user(username="admin", password="1234")

        # Proveedor, revendedor y cliente
        self.proveedor = Proveedor.objects.create(nombre="Proveedor Global", contacto="prov@mail.com", estado=True)
        self.revendedor = Revendedor.objects.create(nombre="Revendedor Global", contacto="rev@mail.com", estado=True)
        self.cliente = Cliente.objects.create(
            nombre="Cliente Global",
            direccion="Av. Mitre 500",
            partido="Morón",
            telefono="111-222"
        )

        # Producto con stock inicial 0
        self.producto = Producto.objects.create(
            nombre="Cocina Global",
            codigo="INT002",
            tipo_gas="envasado",
            precio_pvp=10000,
            estado=True
        )
        self.inventario = Inventario.objects.create(producto=self.producto, stock_actual=0)

    def test_flujo_completo_con_ajuste_y_reporte(self):
        fecha_actual = timezone.now()

        # 1. Confirmar entrada de compra (+10 unidades)
        entrada = CompraEntrada.objects.create(proveedor=self.proveedor, creada_por=self.admin)
        DetalleEntrada.objects.create(entrada=entrada, producto=self.producto, cantidad=10, costo_unitario=8000)
        entrada.confirmar(usuario=self.admin)

        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.stock_actual, 10, "Stock debe incrementarse tras la entrada")

        # 2. Emitir boleta de venta (3 unidades)
        boleta = BoletaVenta.objects.create(
            cliente=self.cliente,
            revendedor=self.revendedor,
            estado="emitida",
            total=30000,
            total_comision=2500,
            costo_envio=0,
            tipo_gas="envasado",
            fecha=fecha_actual
        )
        DetalleBoleta.objects.create(
            boleta=boleta,
            producto=self.producto,
            cantidad=3,
            precio_unitario=10000,
            subtotal=30000,
            comision_item=2500
        )
        ComisionRevendedor.objects.create(
            revendedor=self.revendedor,
            boleta=boleta,
            monto=2500,
            estado="pendiente"
        )

        # Simular salida de stock
        self.inventario.stock_actual -= 3
        self.inventario.save()
        MovimientoInventario.objects.create(
            producto=self.producto,
            tipo="salida",
            cantidad=3,
            referencia=f"Boleta {boleta.id}"
        )

        # 3. Ajuste de inventario (-2 unidades por pérdida)
        self.inventario.stock_actual -= 2
        self.inventario.save()
        MovimientoInventario.objects.create(
            producto=self.producto,
            tipo="salida",
            cantidad=2,
            referencia="Ajuste por pérdida"
        )

        # Validar stock final
        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.stock_actual, 5, "Stock final debe reflejar compra, venta y ajuste")

        # 4. Reporte mensual: solo boletas emitidas
        boletas_mes = BoletaVenta.objects.filter(
            estado="emitida",
            fecha__year=fecha_actual.year,
            fecha__month=fecha_actual.month
        )
        total_ventas = sum(b.total for b in boletas_mes)
        total_comisiones = sum(b.total_comision for b in boletas_mes)

        self.assertEqual(total_ventas, 30000, "El reporte mensual debe reflejar ventas emitidas")
        self.assertEqual(total_comisiones, 2500, "El reporte mensual debe reflejar comisiones emitidas")
