from django.urls import path
from . import views

urlpatterns = [
    path('registrar_materia/', views.registrar_materia, name='registrar_materia'),   
    path('listado_materias/', views.listado_materias, name='listado_materias'),   
    path('editar_materia/<int:id>', views.editar_materia, name='editar_materia'),
    path('eliminar_materia/<int:id>', views.eliminar_materia, name='eliminar_materia'), 
    path('listado_materias/buscar/<str:name>', views.listado_materias_buscar, name='buscar_materia'),     
]