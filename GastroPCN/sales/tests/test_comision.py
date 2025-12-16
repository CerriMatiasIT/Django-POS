# sales/tests/test_comision.py
from django.test import TestCase
from catalog.models import Revendedor, Cliente, Producto
from sales.models import BoletaVenta, DetalleBoleta, ComisionRevendedor

class TestComisionRevendedor(TestCase):
    def setUp(self):
        # Crear cliente y revendedor
        self.cliente = Cliente.objects.create(
            nombre="Carlos Gomez",
            direccion="Av. Mitre 123",
            partido="Morón",
            telefono="444-555"
        )
        self.revendedor = Revendedor.objects.create(
            nombre="Revendedor Test",
            contacto="rev@test.com",
            estado=True
        )

        # Crear producto
        self.producto = Producto.objects.create(
            nombre="Cocina Familiar",
            codigo="COM001",
            tipo_gas="envasado",
            precio_pvp=9000,
            estado=True
        )

        # Crear boleta emitida
        self.boleta = BoletaVenta.objects.create(
            cliente=self.cliente,
            revendedor=self.revendedor,
            estado="emitida",
            total=18000,
            total_comision=1000,
            costo_envio=0,
            tipo_gas="envasado"
        )

        # Crear detalle
        DetalleBoleta.objects.create(
            boleta=self.boleta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=9000,
            subtotal=18000,
            comision_item=1000
        )

        # Crear comisión pendiente
        self.comision = ComisionRevendedor.objects.create(
            revendedor=self.revendedor,
            boleta=self.boleta,
            monto=1000,
            estado="pendiente"
        )

    def test_marcar_comision_como_pagada(self):
        # Validar estado inicial
        self.assertEqual(self.comision.estado, "pendiente", "La comisión debe iniciar como pendiente")

        # Marcar como pagada
        self.comision.estado = "pagado"
        self.comision.save()

        # Validar estado final
        self.comision.refresh_from_db()
        self.assertEqual(self.comision.estado, "pagado", "La comisión debe cambiar a pagado correctamente")
