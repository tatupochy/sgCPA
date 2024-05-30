# attendances/views.py
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from students.models import Course,Student
from payments.models import Enrollment
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.http import HttpResponseBadRequest
from .models import Attendance
from django.urls import reverse
from django.views.generic import DetailView
from django.urls import reverse_lazy
from collections import defaultdict


# sgCPA\attendances\views.py
def registrar_asistencia(request):
    if request.method == 'POST':
        #fecha = request.POST['fecha']
        fecha = request.POST.get('fecha')
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
        #return HttpResponseRedirect(reverse('registrar_asistencia'))
        # Redirige a la vista que muestra las asistencias del curso
        return HttpResponseRedirect(reverse('ver_asistencias', kwargs={'course_id': curso_id}))
    else:
        cursos = Course.objects.all()
        return render(request, 'attendances/registrar_asistencia.html', {'cursos': cursos})


# def alumnos_por_curso(request, course_id):
#     alumnos = Student.objects.filter(course_id=course_id)
#     data = [{'id': alumno.id, 'nombre': alumno.name, 'apellido': alumno.lastName, 'ci': alumno.ciNumber} for alumno in alumnos]
#     return JsonResponse(data, safe=False)

def alumnos_por_curso(request, course_id):
    enrollments = Enrollment.objects.filter(course_id=course_id).select_related('student')
    data = [{'id': enrollment.student.id, 'nombre': enrollment.student.name, 'apellido': enrollment.student.lastName, 'ci': enrollment.student.ciNumber} for enrollment in enrollments]
    return JsonResponse(data, safe=False)


def ver_asistencias(request, course_id):
    # Obtener el curso especificado por course_id
    curso = get_object_or_404(Course, pk=course_id)
    
    # Obtener todas las fechas únicas de asistencia para el curso especificado
    fechas = Attendance.objects.filter(course=curso).order_by('date').values_list('date', flat=True).distinct()

    # Obtener todos los estudiantes asociados al curso
    #alumnos = curso.student_set.all()
    enrollments = Enrollment.objects.filter(course=curso).select_related('student')
    alumnos = [enrollment.student for enrollment in enrollments]
    
    # Crear una lista de asistencias por estudiantes
    lista_asistencias = []
    for alumno in alumnos:
        asistencias_alumno = []
        for fecha in fechas:
            # Verificar si el estudiante estuvo presente en esta fecha
            asistencia = Attendance.objects.filter(student=alumno, date=fecha, present=True).exists()
            if asistencia:
                asistencias_alumno.append('P')
            else:
                asistencias_alumno.append('A')
        lista_asistencias.append({'alumno': alumno, 'asistencias': asistencias_alumno})

    return render(request, 'attendances/ver_asistencias.html', {'curso': curso, 'fechas': fechas, 'lista_asistencias': lista_asistencias})


def actualizar_asistencia(request, attendance_id):
    attendance = get_object_or_404(Attendance, pk=attendance_id)
    cursos = Course.objects.filter(id=attendance.course.id)  # Filtrar el curso específico

    if request.method == 'POST':
        # Procesar los datos enviados por el formulario
        fecha = request.POST.get('fecha')
        #present = request.POST.get('present')
        present = request.POST.get('present', False) == 'true'

        # Actualizar los campos de la asistencia
        attendance.date = fecha
        attendance.present = present
        attendance.save()

        # Redirigir a alguna página de confirmación o a donde sea necesario
        return redirect(f'/actualizar_asistencia/{attendance_id}/?registrado=true')  # Reemplaza 'pagina_confirmacion' con la URL adecuada
    else:
        # Si no hay datos enviados por POST, cargar la página con los datos actuales de la asistencia
        return render(request, 'attendances/actualizar_asistencia.html', {'attendance': attendance})

def eliminar_asistencia(request, attendance_id):
    if request.method == 'DELETE':
        # Obtener la asistencia a eliminar
        asistencia = get_object_or_404(Attendance, pk=attendance_id)
        print(attendance_id)
        # Eliminar la asistencia de la base de datos
        asistencia.delete()
        
        # Devolver una respuesta exitosa
        return JsonResponse({'mensaje': 'Asistencia eliminada correctamente'}, status=200)
    else:
        # Devolver un error si la solicitud no es DELETE
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def listado_asistencias(request):
    cursos = Course.objects.all()
    alumnos = []
    asistencias = []

    if request.method == 'POST':
        curso_id = request.POST.get('curso_id')
        if curso_id:
            curso = Course.objects.get(pk=curso_id)
            alumnos = Student.objects.filter(course=curso)
            asistencias = Attendance.objects.filter(course=curso).order_by('date')
            #fechas = Attendance.objects.filter(course=curso).order_by('date').values_list('date', flat=True).distinct()
    return render(request, 'attendances/listado_asistencias.html', {'cursos': cursos, 'alumnos': alumnos, 'asistencias': asistencias})