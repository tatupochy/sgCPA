# attendances/views.py
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from students.models import Course,Student
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.http import HttpResponseBadRequest
from .models import Attendance
from django.urls import reverse
from django.views.generic import DetailView
from django.urls import reverse_lazy

# sgCPA\attendances\views.py
def registrar_asistencia(request):
    if request.method == 'POST':
        fecha = request.POST['fecha']
        curso_id = request.POST['curso']
        curso = Course.objects.get(pk=curso_id)
        
        # Recorre todas las claves del diccionario POST
        for key, value in request.POST.items():
            # Verifica si la clave comienza con 'presente_', indicando que es un checkbox de asistencia
            if key.startswith('presente_'):
                alumno_id = key.split('_')[1]  # Obtiene el ID del alumno de la clave
                alumno = Student.objects.get(pk=alumno_id)
                # Convierte el valor 'true'/'false' en un valor booleano
                presente = value == 'true'
                Attendance.objects.create(date=fecha, course=curso, student=alumno, present=presente)
        
        return HttpResponseRedirect(reverse('home'))
    else:
        cursos = Course.objects.all()
        return render(request, 'attendances/registrar_asistencia.html', {'cursos': cursos})


def alumnos_por_curso(request, course_id):
    alumnos = Student.objects.filter(course_id=course_id)
    data = [{'id': alumno.id, 'nombre': alumno.name, 'apellido': alumno.lastName, 'ci': alumno.ciNumber} for alumno in alumnos]
    return JsonResponse(data, safe=False)
