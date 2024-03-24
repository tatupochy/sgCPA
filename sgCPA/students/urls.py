from django.urls import path
from . import views

urlpatterns = [
    path('registrar_alumno/', views.registrar_alumno, name='registrar_alumno'),
    path('listado_alumnos', views.listado_alumnos, name="listado_alumnos"),
    path('listado_alumnos/buscar/<str:id>', views.buscar, name="buscar"),
    path('editar_alumno/<int:id>', views.editar_alumno),
    path('eliminar/<int:id>', views.eliminar, name="eliminar"),

    path('registrar_curso/', views.registrar_curso),
    path('detalle_curso/<int:id>/', views.detalle_curso, name='detalle_curso'), 
    path('editar_curso/<int:id>/', views.editar_curso, name='editar_curso'),
    path('borrar_curso/<int:id>/', views.borrar_curso, name='borrar_curso'),
    path('listar_curso/', views.listar_curso, name='listar_curso'),
    
]