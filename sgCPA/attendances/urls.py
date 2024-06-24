# sgCPA\attendances\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registrar_asistencia/', views.registrar_asistencia, name='registrar_asistencia'), #que sea para admins
    path('registrar_asistencia2/', views.registrar_asistencia2, name='registrar_asistencia2'), #que sea para otros (secretarios/docentes)
    path('alumnos_por_curso/<int:course_id>', views.alumnos_por_curso, name='alumnos_por_curso'),
    path('ver_asistencias/<int:course_id>/', views.ver_asistencias, name='ver_asistencias'),
    path('actualizar_asistencia/<int:attendance_id>/', views.actualizar_asistencia, name='actualizar_asistencia'),
    path('eliminar_asistencia/<int:attendance_id>/', views.eliminar_asistencia, name='eliminar_asistencia'),
    path('listado_asistencias/', views.listado_asistencias, name='listado_asistencias'),
    path('obtener_fechas_curso/<int:curso_id>', views.obtener_fechas_curso),
    path('obtener_fechas_curso2/<int:curso_id>', views.obtener_fechas_curso2),
    # path('obtener_asistencias/<int:id>/<int:day>/<int:month>/<int:year>/', views.obtener_asistencias)
    path('obtener_asistencias/<int:id>', views.obtener_asistencias,name='obtener_asistencias'),
    # path('obtener_meses_curso/<int:curso_id>/',  views.obtener_meses_curso, name='obtener_meses_curso'),
    # path('ver_asistencias_fecha/', views.ver_asistencias_fecha, name='ver_asistencias_fecha'),
    path('descargar_asistencias_pdf', views.descargar_asistencias_pdf, name='descargar_asistencias_pdf')
]
