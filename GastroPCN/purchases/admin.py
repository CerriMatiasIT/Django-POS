from django.contrib import admin
from .models import CompraEntrada, DetalleEntrada

class DetalleEntradaInline(admin.TabularInline):
    model = DetalleEntrada
    extra = 1

@admin.register(CompraEntrada)
class CompraEntradaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "proveedor", "total")
    search_fields = ("proveedor__nombre",)
    inlines = [DetalleEntradaInline]
