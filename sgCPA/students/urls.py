from django.urls import path
from . import views

urlpatterns = [
    path('registrar_alumno/', views.registrar_alumno, name='registrar_alumno'),
    path('registrar_curso/', views.registrar_curso),
    path('detalle_curso/<int:id>/', views.detalle_curso, name='detalle_curso'),
    path('listado_alumnos', views.listado_alumnos, name="listado_alumnos"),
    path('editar_alumno/<int:id>', views.editar_alumno),
    path('eliminar/<int:id>', views.eliminar, name="eliminar")
]