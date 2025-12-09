from django.contrib import admin
from .models import Inventario, MovimientoInventario

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ("producto", "stock_actual")
    search_fields = ("producto__nombre",)

@admin.register(MovimientoInventario)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("producto", "tipo", "cantidad", "fecha", "referencia")
    list_filter = ("tipo", "fecha")
    search_fields = ("producto__nombre", "referencia")
