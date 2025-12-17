# integration/tests/test_flujo_completo.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import Cliente, Revendedor, Producto, Proveedor
from inventory.models import Inventario, MovimientoInventario
from purchases.models import CompraEntrada, DetalleEntrada
from sales.models import BoletaVenta, DetalleBoleta, ComisionRevendedor

User = get_user_model()

class TestFlujoCompleto(TestCase):
    def setUp(self):
        # Usuario admin
        self.admin = User.objects.create_user(username="admin", password="1234")

        # Proveedor y revendedor
        self.proveedor = Proveedor.objects.create(nombre="Proveedor X", contacto="provx@mail.com", estado=True)
        self.revendedor = Revendedor.objects.create(nombre="Revendedor Y", contacto="rev@mail.com", estado=True)

        # Cliente
        self.cliente = Cliente.objects.create(
            nombre="Cliente Z",
            direccion="Av. Rivadavia 1000",
            partido="Morón",
            telefono="555-666"
        )

        # Producto con stock inicial 0
        self.producto = Producto.objects.create(
            nombre="Cocina Integrada",
            codigo="INT001",
            tipo_gas="envasado",
            precio_pvp=12000,
            estado=True
        )
        self.inventario = Inventario.objects.create(producto=self.producto, stock_actual=0)

    def test_flujo_completo_compras_ventas_inventario(self):
        # 1. Confirmar entrada de compra (+5 unidades)
        entrada = CompraEntrada.objects.create(proveedor=self.proveedor, creada_por=self.admin)
        DetalleEntrada.objects.create(entrada=entrada, producto=self.producto, cantidad=5, costo_unitario=10000)
        entrada.confirmar(usuario=self.admin)

        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.stock_actual, 5, "El stock debe incrementarse tras la entrada")

        # 2. Emitir boleta de venta (2 unidades)
        boleta = BoletaVenta.objects.create(
            cliente=self.cliente,
            revendedor=self.revendedor,
            estado="emitida",
            total=24000,
            total_comision=2000,
            costo_envio=0,
            tipo_gas="envasado"
        )
        DetalleBoleta.objects.create(
            boleta=boleta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=12000,
            subtotal=24000,
            comision_item=2000
        )
        ComisionRevendedor.objects.create(
            revendedor=self.revendedor,
            boleta=boleta,
            monto=2000,
            estado="pendiente"
        )

        # Simular salida de stock
        self.inventario.stock_actual -= 2
        self.inventario.save()
        MovimientoInventario.objects.create(
            producto=self.producto,
            tipo="salida",
            cantidad=2,
            referencia=f"Boleta {boleta.id}"
        )

        # 3. Validar stock final
        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.stock_actual, 3, "El stock debe reflejar la venta")

        # 4. Validar movimiento de entrada y salida
        movimientos = MovimientoInventario.objects.filter(producto=self.producto)
        self.assertEqual(movimientos.count(), 2, "Debe haber dos movimientos: entrada y salida")

        # 5. Validar comisión pendiente
        comision = ComisionRevendedor.objects.filter(boleta=boleta).first()
        self.assertEqual(comision.estado, "pendiente", "La comisión debe quedar registrada como pendiente")
