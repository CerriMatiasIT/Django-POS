# Sistema de Gestión de Cocinas Industriales

Este proyecto en **Django 5.2** permite gestionar ventas, compras, inventario y comisiones de revendedores para un negocio de cocinas industriales.

## 🚀 Características principales
- Control de inventario con entradas y salidas de mercadería.
- Emisión de boletas con cálculo automático de comisiones y costos de envío.
- Registro de compras y proveedores.
- Reportes mensuales de ventas y efectivo.
- Administración de usuarios y auditoría básica.

## 📂 Estructura del proyecto
- `core/` → usuarios y auditoría
- `catalog/` → productos, clientes, revendedores, proveedores, tarifas de envío
- `inventory/` → stock y movimientos
- `sales/` → boletas, comisiones, reportes mensuales
- `purchases/` → entradas de mercadería

## ⚙️ Instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tuusuario/cocinas.git
   cd cocinas
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

## 👥 Usuarios
Tres administradores con acceso total.

Un empleado que opera con credenciales de administrador.

## 📌 Próximos pasos
Formularios de “Nueva boleta” y “Nueva entrada”.

Reportes mensuales y pantalla de comisiones.

API REST con Django REST Framework.

Pruebas unitarias de emisión, anulación y confirmación de entradas.
