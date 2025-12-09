from django.contrib import admin
from .models import Producto, Cliente, Revendedor, Proveedor, TarifaEnvio

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo", "tipo_gas", "precio_pvp", "estado")
    list_filter = ("tipo_gas", "estado")
    search_fields = ("nombre", "codigo")

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "direccion", "partido", "telefono")
    search_fields = ("nombre", "partido")

@admin.register(Revendedor)
class RevendedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "contacto", "estado")
    list_filter = ("estado",)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "contacto", "estado")
    list_filter = ("estado",)

@admin.register(TarifaEnvio)
class TarifaEnvioAdmin(admin.ModelAdmin):
    list_display = ("localidad", "precio_sugerido", "fletero")
    search_fields = ("localidad", "fletero")
