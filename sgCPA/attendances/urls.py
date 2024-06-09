# sgCPA\attendances\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registrar_asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('alumnos_por_curso/<int:course_id>', views.alumnos_por_curso, name='alumnos_por_curso'),
    #path('ver_asistencias/', views.ver_asistencias, name='ver_asistencias'),
    path('ver_asistencias/<int:course_id>/', views.ver_asistencias, name='ver_asistencias'),
    path('actualizar_asistencia/<int:attendance_id>/', views.actualizar_asistencia, name='actualizar_asistencia'),
    path('eliminar_asistencia/<int:attendance_id>/', views.eliminar_asistencia, name='eliminar_asistencia'),
    path('listado_asistencias/', views.listado_asistencias, name='listado_asistencias'),
    path('obtener_meses_curso/<int:curso_id>/',  views.obtener_meses_curso, name='obtener_meses_curso'),

    path('ver_asistencias_fecha/', views.ver_asistencias_fecha, name='ver_asistencias_fecha'),
    path('descargar_asistencias_pdf/<int:curso_id>/<str:fecha>/', views.descargar_asistencias_pdf, name='descargar_asistencias_pdf'),


]
