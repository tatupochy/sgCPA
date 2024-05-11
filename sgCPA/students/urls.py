from django.urls import path
from . import views

urlpatterns = [
    path('registrar_alumno/', views.registrar_alumno, name='registrar_alumno'),
    path('listado_alumnos', views.listado_alumnos, name="listado_alumnos"),
    path('listado_alumnos/buscar/<str:id>', views.buscar, name="buscar"),
    path('editar_alumno/<int:id>', views.editar_alumno),
    path('eliminar/<int:id>', views.eliminar, name="eliminar"),
    path('listado_alumnos/<int:curso_id>/', views.listado_alumnos, name='listado_alumnos'), ##add

    path('registrar_curso/', views.registrar_curso),
    path('detalle_curso/<int:id>/', views.detalle_curso, name='detalle_curso'), 
    path('editar_curso/<int:id>/', views.editar_curso, name='editar_curso'),
    path('borrar_curso/<int:id>/', views.borrar_curso, name='borrar_curso'),
    path('listar_curso/', views.listar_curso, name='listar_curso'),

    path('sections/', views.section_list, name='sections'),
    path('sections/create/', views.section_create, name='section_create'),
    path('sections/<int:id>/', views.section_detail, name='section_detail'),
    path('sections/<int:id>/edit/', views.section_edit, name='section_update'),
    path('sections/<int:id>/delete/', views.section_delete, name='section_delete'),

    path('shifts/', views.shift_list, name='shifts'),
    path('shifts/create/', views.shift_create, name='shift_create'),
    path('shifts/<int:id>/', views.shift_detail, name='shift_detail'),
    path('shifts/<int:id>/edit/', views.shift_edit, name='shift_update'),
    path('shifts/<int:id>/delete/', views.shift_delete, name='shift_delete'),
    
]