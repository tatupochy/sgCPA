# sgCPA\attendances\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registrar_asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('alumnos_por_curso/<int:course_id>', views.alumnos_por_curso, name='alumnos_por_curso'),
]
