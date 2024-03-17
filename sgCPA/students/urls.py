from django.urls import path
from . import views

urlpatterns = [
    path('registrar_alumno/', views.registrar_alumno),
    path('registrar_curso/', views.registrar_curso),
    path('detalle_curso/<int:id>/', views.detalle_curso, name='detalle_curso'),
]