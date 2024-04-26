from django.urls import path
from . import views

urlpatterns = [
    path('registrar_ciudad/', views.registrar_ciudad),
    path('listado_ciudades', views.listado_ciudades),
    path('borrar_ciudad/<int:id>', views.borrar_ciudad),
    path('editar_ciudad/<int:id>', views.editar_ciudad)
]