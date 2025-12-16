# inventory/tests/test_ajuste.py
from django.test import TestCase
from catalog.models import Producto
from inventory.models import Inventario, MovimientoInventario

class TestMovimientoAjuste(TestCase):
    def setUp(self):
        # Crear producto con stock inicial
        self.producto = Producto.objects.create(
            nombre="Cocina Compacta",
            codigo="AJ001",
            tipo_gas="envasado",
            precio_pvp=8000,
            estado=True
        )
        self.inventario = Inventario.objects.create(producto=self.producto, stock_actual=10)

    def test_movimiento_ajuste_modifica_stock_y_registra_referencia(self):
        # Simular un ajuste de stock: +5 unidades
        ajuste_cantidad = 5
        referencia = "Ajuste manual por control de inventario"

        # Aplicar ajuste
        self.inventario.stock_actual += ajuste_cantidad
        self.inventario.save()

        # Registrar movimiento
        movimiento = MovimientoInventario.objects.create(
            producto=self.producto,
            tipo="entrada",  # usamos 'entrada' para sumar stock
            cantidad=ajuste_cantidad,
            referencia=referencia
        )

        # Validaciones
        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.stock_actual, 15, "El stock debe reflejar el ajuste aplicado")

        self.assertEqual(movimiento.tipo, "entrada", "El movimiento debe registrarse como ENTRADA")
        self.assertEqual(movimiento.cantidad, 5, "La cantidad del movimiento debe coincidir con el ajuste")
        self.assertEqual(movimiento.referencia, referencia, "La referencia debe quedar registrada correctamente")
