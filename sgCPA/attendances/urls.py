# sgCPA\attendances\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registrar_asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('alumnos_por_curso/<int:course_id>', views.alumnos_por_curso, name='alumnos_por_curso'),
    path('ver_asistencias/<int:course_id>/', views.ver_asistencias, name='ver_asistencias'),
    path('actualizar_asistencia/<int:attendance_id>/', views.actualizar_asistencia, name='actualizar_asistencia'),
    path('eliminar_asistencia/<int:attendance_id>/', views.eliminar_asistencia, name='eliminar_asistencia'),
    path('listado_asistencias/', views.listado_asistencias, name='listado_asistencias'),
    path('obtener_fechas_curso/<int:curso_id>', views.obtener_fechas_curso),
    # path('obtener_asistencias/<int:id>/<int:day>/<int:month>/<int:year>/', views.obtener_asistencias)
    path('obtener_asistencias/<int:id>', views.obtener_asistencias)
]
