# inventory/tests/test_ajuste_negativo.py
from django.test import TestCase
from catalog.models import Producto
from inventory.models import Inventario, MovimientoInventario

class TestMovimientoAjusteNegativo(TestCase):
    def setUp(self):
        # Crear producto con stock inicial
        self.producto = Producto.objects.create(
            nombre="Cocina Industrial",
            codigo="AJ002",
            tipo_gas="envasado",
            precio_pvp=10000,
            estado=True
        )
        self.inventario = Inventario.objects.create(producto=self.producto, stock_actual=20)

    def test_movimiento_ajuste_negativo_registra_salida_y_disminuye_stock(self):
        # Simular un ajuste negativo: -4 unidades
        ajuste_cantidad = 4
        referencia = "Ajuste por pérdida de mercadería"

        # Aplicar ajuste
        self.inventario.stock_actual -= ajuste_cantidad
        self.inventario.save()

        # Registrar movimiento
        movimiento = MovimientoInventario.objects.create(
            producto=self.producto,
            tipo="salida",  # usamos 'salida' para restar stock
            cantidad=ajuste_cantidad,
            referencia=referencia
        )

        # Validaciones
        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.stock_actual, 16, "El stock debe disminuir tras el ajuste negativo")

        self.assertEqual(movimiento.tipo, "salida", "El movimiento debe registrarse como SALIDA")
        self.assertEqual(movimiento.cantidad, 4, "La cantidad del movimiento debe coincidir con el ajuste negativo")
        self.assertEqual(movimiento.referencia, referencia, "La referencia debe quedar registrada correctamente")
