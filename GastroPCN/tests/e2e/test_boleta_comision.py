# tests/e2e/test_boleta_comision.py
import pytest
from playwright.sync_api import sync_playwright

def test_flujo_revendedor_boleta_comision():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Login como revendedor
        page.goto("http://localhost:8000/login/")
        page.fill("input[name='username']", "revendedor_test")
        page.fill("input[name='password']", "1234")
        page.click("button[type='submit']")

        # 2. Crear boleta
        page.goto("http://localhost:8000/boletas/nueva/")
        page.select_option("select[name='cliente']", "Cliente Z")
        page.select_option("select[name='producto']", "Cocina Premium")
        page.fill("input[name='cantidad']", "2")
        page.click("button[type='submit']")

        # Validar boleta creada
        assert "Boleta creada" in page.text_content("body")

        # 3. Validar comisión calculada
        page.goto("http://localhost:8000/comisiones/")
        assert "pendiente" in page.text_content("body")

        # 4. Marcar comisión como pagada
        page.click("button[name='marcar_pagada']")
        assert "pagado" in page.text_content("body")

        # 5. Validar reporte mensual
        page.goto("http://localhost:8000/reportes/mensual/")
        assert "Total Ventas" in page.text_content("body")
        assert "Total Comisiones" in page.text_content("body")

        browser.close()
