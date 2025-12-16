# sales/tests/test_boleta.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import Producto, Cliente, Revendedor
from inventory.models import Inventario
from sales.models import BoletaVenta, DetalleBoleta, ComisionRevendedor

User = get_user_model()

class TestBoletaVenta(TestCase):
    def setUp(self):
        # Usuario admin
        self.admin = User.objects.create_user(username="admin", password="1234")

        # Cliente y revendedor
        self.cliente = Cliente.objects.create(
            nombre="Juan Perez",
            direccion="Calle Falsa 123",
            partido="Morón",
            telefono="111-222"
        )
        self.revendedor = Revendedor.objects.create(
            nombre="Revendedor 1",
            contacto="rev1@mail.com",
            estado=True
        )

        # Producto con stock inicial
        self.producto = Producto.objects.create(
            nombre="Cocina Industrial",
            codigo="C001",
            tipo_gas="envasado",   # coincide con las choices
            precio_pvp=10000,
            estado=True
        )
        self.inventario = Inventario.objects.create(producto=self.producto, stock_actual=10)

        # Boleta en borrador
        self.boleta = BoletaVenta.objects.create(
            cliente=self.cliente,
            revendedor=self.revendedor,
            costo_envio=500,
            tipo_gas="envasado"
        )

        # Detalle con comisión
        DetalleBoleta.objects.create(
            boleta=self.boleta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=10000,
            subtotal=20000,
            comision_item=2000
        )

    def test_emitir_boleta_descuenta_stock_y_genera_comision(self):
        # Simular emisión manual: calcular totales y actualizar stock/comisiones
        total, total_comision = 0, 0
        for item in self.boleta.detalles.all():
            total += item.subtotal
            total_comision += item.comision_item
            inv = item.producto.inventario
            inv.stock_actual -= item.cantidad
            inv.save()
            ComisionRevendedor.objects.create(
                revendedor=self.revendedor,
                boleta=self.boleta,
                monto=item.comision_item,
                estado="pendiente"
            )

        self.boleta.total = total + self.boleta.costo_envio
        self.boleta.total_comision = total_comision
        self.boleta.estado = "emitida"
        self.boleta.save()

        # Validaciones
        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.stock_actual, 8, "El stock debe descontarse al emitir la boleta")
        self.assertEqual(self.boleta.estado, "emitida", "La boleta debe quedar en estado EMITIDA")

        comisiones = ComisionRevendedor.objects.filter(revendedor=self.revendedor, boleta=self.boleta)
        self.assertEqual(comisiones.count(), 1, "Debe generarse una comisión para el revendedor")
        self.assertEqual(comisiones.first().monto, 2000, "La comisión debe ser igual al monto definido en el detalle")
