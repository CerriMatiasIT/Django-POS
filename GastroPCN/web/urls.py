from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("boletas/nueva/", views.boleta_nueva, name="boleta_nueva"),
    path("comisiones/", views.comisiones, name="comisiones"),
    path("reportes/mensual/", views.reporte_mensual, name="reporte_mensual"),
]
