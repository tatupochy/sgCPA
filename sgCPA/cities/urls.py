from django.urls import path
from . import views

urlpatterns = [
    path('registrar_ciudad/', views.registrar_ciudad),
    # path('listado_ciudades', views.listado_ciudades),
    path('borrar_ciudad/<int:id>', views.borrar_ciudad),
    path('editar_ciudad/<int:id>', views.editar_ciudad),
    path('obtener_ciudades_por_pais/<int:id>', views.obtener_ciudades_por_pais),
    path('listado_ciudades', views.listado_ciudades)
]