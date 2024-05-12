from django.urls import path
from . import views

urlpatterns = [
    path('registrar_pais/', views.registrar_pais),
    path('listado_paises', views.listado_paises),
    path('inhabilitar_pais/<int:id>', views.borrar_pais),
    path('editar_pais/<int:id>', views.editar_pais)   
]