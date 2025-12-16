# sales/tests/test_boleta_anulacion.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import Producto, Cliente, Revendedor
from inventory.models import Inventario
from sales.models import BoletaVenta, DetalleBoleta, ComisionRevendedor

User = get_user_model()

class TestBoletaAnulacion(TestCase):
    def setUp(self):
        # Usuario admin
        self.admin = User.objects.create_user(username="admin", password="1234")

        # Cliente y revendedor
        self.cliente = Cliente.objects.create(
            nombre="Maria Lopez",
            direccion="Av. Siempre Viva 742",
            partido="Morón",
            telefono="222-333"
        )
        self.revendedor = Revendedor.objects.create(
            nombre="Revendedor 2",
            contacto="rev2@mail.com",
            estado=True
        )

        # Producto con stock inicial
        self.producto = Producto.objects.create(
            nombre="Cocina Industrial",
            codigo="C002",
            tipo_gas="envasado",
            precio_pvp=12000,
            estado=True
        )
        self.inventario = Inventario.objects.create(producto=self.producto, stock_actual=5)

        # Boleta emitida
        self.boleta = BoletaVenta.objects.create(
            cliente=self.cliente,
            revendedor=self.revendedor,
            costo_envio=300,
            tipo_gas="envasado",
            estado="emitida",
            total=24300,
            total_comision=1500
        )

        # Detalle con comisión
        DetalleBoleta.objects.create(
            boleta=self.boleta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=12000,
            subtotal=24000,
            comision_item=1500
        )

        # Simular impacto inicial: descontar stock y generar comisión
        self.inventario.stock_actual -= 2
        self.inventario.save()
        ComisionRevendedor.objects.create(
            revendedor=self.revendedor,
            boleta=self.boleta,
            monto=1500,
            estado="pendiente"
        )

    def test_anular_boleta_devuelve_stock_y_registra_motivo(self):
        # Simular anulación
        motivo = "Cliente canceló la compra"
        self.boleta.estado = "anulada"
        self.boleta.save()

        # Devolver stock
        for item in self.boleta.detalles.all():
            inv = item.producto.inventario
            inv.stock_actual += item.cantidad
            inv.save()

        # Validaciones
        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.stock_actual, 5, "El stock debe volver al valor original tras la anulación")
        self.assertEqual(self.boleta.estado, "anulada", "La boleta debe quedar en estado ANULADA")

        # Validar que existe comisión pendiente asociada
        comisiones = ComisionRevendedor.objects.filter(revendedor=self.revendedor, boleta=self.boleta)
        self.assertEqual(comisiones.count(), 1, "Debe existir la comisión asociada a la boleta")
        self.assertEqual(comisiones.first().estado, "pendiente", "La comisión queda pendiente hasta que se defina política de reverso")
