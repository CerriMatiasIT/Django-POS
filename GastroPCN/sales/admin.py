from django.contrib import admin
from .models import BoletaVenta, DetalleBoleta, ComisionRevendedor

class DetalleBoletaInline(admin.TabularInline):
    model = DetalleBoleta
    extra = 1

@admin.register(BoletaVenta)
class BoletaVentaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "cliente", "revendedor", "estado", "total")
    list_filter = ("estado", "revendedor")
    search_fields = ("cliente__nombre", "revendedor__nombre")
    inlines = [DetalleBoletaInline]

    actions = ["anular_boleta"]

    def anular_boleta(self, request, queryset):
        for boleta in queryset:
            boleta.estado = "anulada"
            boleta.save()
        self.message_user(request, "Boletas anuladas correctamente.")
    anular_boleta.short_description = "Anular boletas seleccionadas"


@admin.register(ComisionRevendedor)
class ComisionAdmin(admin.ModelAdmin):
    list_display = ("revendedor", "boleta", "monto", "estado", "fecha")
    list_filter = ("estado", "revendedor")
    actions = ["marcar_como_pagado"]

    def marcar_como_pagado(self, request, queryset):
        queryset.update(estado="pagado")
        self.message_user(request, "Comisiones marcadas como pagadas.")
    marcar_como_pagado.short_description = "Marcar comisiones seleccionadas como pagadas"
