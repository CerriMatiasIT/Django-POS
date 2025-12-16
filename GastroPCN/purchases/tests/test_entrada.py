# purchases/tests/test_entrada.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import Producto, Proveedor
from inventory.models import Inventario, MovimientoInventario
from purchases.models import CompraEntrada, DetalleEntrada

User = get_user_model()

class TestConfirmarEntrada(TestCase):
    def setUp(self):
        # Usuario admin
        self.admin = User.objects.create_user(username="admin", password="1234")

        # Proveedor
        self.proveedor = Proveedor.objects.create(
            nombre="Proveedor X",
            contacto="provx@mail.com",
            estado=True
        )

        # Producto con stock inicial
        self.producto = Producto.objects.create(
            nombre="Cocina Industrial",
            codigo="P001",
            tipo_gas="envasado",
            precio_pvp=15000,
            estado=True
        )
        self.inventario = Inventario.objects.create(producto=self.producto, stock_actual=5)

        # Entrada en borrador
        self.entrada = CompraEntrada.objects.create(
            proveedor=self.proveedor,
            creada_por=self.admin
        )

        # Detalle de entrada
        DetalleEntrada.objects.create(
            entrada=self.entrada,
            producto=self.producto,
            cantidad=3,
            costo_unitario=12000
        )

    def test_confirmar_entrada_incrementa_stock_y_registra_movimiento(self):
        # Confirmar entrada
        self.entrada.confirmar(usuario=self.admin)

        # Validar stock incrementado
        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.stock_actual, 8, "El stock debe incrementarse al confirmar la entrada")

        # Validar movimiento registrado
        movimiento = MovimientoInventario.objects.filter(
            producto=self.producto,
            referencia__contains=f"Entrada {self.entrada.id}"
        ).first()

        self.assertIsNotNone(movimiento, "Debe registrarse un movimiento de inventario")
        self.assertEqual(movimiento.tipo, "entrada", "El movimiento debe ser de tipo ENTRADA")
        self.assertEqual(movimiento.cantidad, 3, "La cantidad del movimiento debe coincidir con el detalle")
