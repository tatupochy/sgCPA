from django.urls import path
from . import views

urlpatterns = [
    path('registrar_alumno/', views.registrar_alumno)
]