# attendances/views.py
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from students.models import Course,Student
from payments.models import Enrollment
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.http import HttpResponse
from .models import Attendance
from django.urls import reverse
from django.views.generic import DetailView
from django.urls import reverse_lazy
from collections import defaultdict
from .utils import check_attendance,calcular_asistencia_mes,get_business_days,get_business_days_in_month,get_expected_attendance_days
from calendar import monthrange, month_name
from datetime import datetime, timedelta, date


from django.template.loader import render_to_string
from xhtml2pdf import pisa


# sgCPA\attendances\views.py
def registrar_asistencia(request):
    if request.method == 'POST':
        #fecha = request.POST['fecha']
        fecha = request.POST.get('fecha')
        curso_id = request.POST['curso']
        curso = Course.objects.get(pk=curso_id)

        # Obtener todos los alumnos del curso a través de Enrollment
        enrollments = Enrollment.objects.filter(course_id=curso_id).select_related('student')
        alumnos_curso = [enrollment.student for enrollment in enrollments]
        
        # Recorre todas las claves del diccionario POST
        for key, value in request.POST.items():
            # Verifica si la clave comienza con 'presente_', indicando que es un checkbox de asistencia
            if key.startswith('presente_'):
                alumno_id = key.split('_')[1]  # Obtiene el ID del alumno de la clave
                alumno = Student.objects.get(pk=alumno_id)
                # Convierte el valor 'true'/'false' en un valor booleano
                presente = value == 'true'
                Attendance.objects.create(date=fecha, course=curso, student=alumno, present=presente)

                # Remover al alumno de la lista de alumnos del curso
                if alumno in alumnos_curso:
                    alumnos_curso.remove(alumno)


        # Registrar asistencia con valor False para los alumnos restantes
        for alumno in alumnos_curso:
            Attendance.objects.create(date=fecha, course=curso, student=alumno, present=False)

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

# def listado_asistencias(request):
#     cursos = Course.objects.all()
#     alumnos = []
#     asistencias = []

#     if request.method == 'POST':
#         curso_id = request.POST.get('curso_id')
#         if curso_id:
#             curso = Course.objects.get(pk=curso_id)
#             #alumnos = Student.objects.filter(course=curso)
#             enrollments = Enrollment.objects.filter(course=curso).select_related('student')
#             alumnos = [enrollment.student for enrollment in enrollments]
#             asistencias = Attendance.objects.filter(course=curso).order_by('date')
#             #fechas = Attendance.objects.filter(course=curso).order_by('date').values_list('date', flat=True).distinct()
#     return render(request, 'attendances/listado_asistencias.html', {'cursos': cursos, 'alumnos': alumnos, 'asistencias': asistencias})

def listado_asistencias(request):
    cursos = Course.objects.all()
    alumnos = []
    asistencias = []
    low_attendance_students = defaultdict(list)
    meses_curso = []
    selected_curso = None
    selected_mes = None

    if request.method == 'POST':
        curso_id = request.POST.get('curso_id')
        selected_mes = request.POST.get('mes')
        if selected_mes:
            selected_mes = int(selected_mes)

        if curso_id:
            selected_curso = Course.objects.get(pk=curso_id)
            enrollments = Enrollment.objects.filter(course=selected_curso).select_related('student')
            alumnos = [enrollment.student for enrollment in enrollments]
            asistencias = Attendance.objects.filter(course=selected_curso).order_by('date')

            # Obtener los meses del rango del curso
            start_month = selected_curso.start_date.month
            end_month = selected_curso.end_date.month
            meses_curso = [(m, month_name[m]) for m in range(start_month, end_month + 1)]

            # Excluir el mes actual
            current_year = date.today().year
            current_month = date.today().month
            if selected_mes and selected_mes <= current_month and selected_curso.end_date.year == current_year:
                asistencias = asistencias.filter(date__month=selected_mes)
            else:
                asistencias = asistencias.none()  # No mostrar asistencias si el mes es el actual o futuro

            for alumno in alumnos:
                for month in range(start_month, end_month + 1):
                    # Calcular solo para meses anteriores al mes actual
                    if month < current_month or selected_curso.end_date.year < current_year:
                        year = selected_curso.end_date.year
                        dias_por_semana = selected_curso.days_per_week
                        expected_classes = get_business_days_in_month(year, month, dias_por_semana)
                        asistencia_mes = calcular_asistencia_mes(alumno.id, month, selected_curso)
                        if asistencia_mes < 0.7 * expected_classes:
                            low_attendance_students[alumno.id].append(month)

    return render(request, 'attendances/listado_asistencias.html', {
        'cursos': cursos,
        'alumnos': alumnos,
        'asistencias': asistencias,
        'low_attendance_students': low_attendance_students,
        'meses_curso': meses_curso,
        'selected_curso': selected_curso,
        'selected_mes': selected_mes,
    })

def obtener_meses_curso(request, curso_id):
    curso = get_object_or_404(Course, pk=curso_id)
    start_month = curso.start_date.month
    end_month = curso.end_date.month
    meses_curso = [(m, month_name[m]) for m in range(start_month, end_month + 1)]
    return JsonResponse({'meses_curso': meses_curso})

#08/06/2024x1
def ver_asistencias_fecha(request):
    cursos = Course.objects.filter(active=True)
    asistencias = []
    selected_curso = None
    selected_fecha = None

    if request.method == 'POST':
        curso_id = request.POST.get('curso_id')
        fecha = request.POST.get('fecha')

        if curso_id and fecha:
            selected_curso = get_object_or_404(Course, pk=curso_id)
            selected_fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            asistencias = Attendance.objects.filter(course=selected_curso, date=selected_fecha)

    return render(request, 'attendances/ver_asistencias_fecha.html', {
        'cursos': cursos,
        'asistencias': asistencias,
        'selected_curso': selected_curso,
        'selected_fecha': selected_fecha,
    })

def descargar_asistencias_pdf(request, curso_id, fecha):
    curso = get_object_or_404(Course, pk=curso_id)
    fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
    asistencias = Attendance.objects.filter(course=curso, date=fecha)

    # Preparar el contexto para el template
    context = {
        'curso': curso,
        'fecha': fecha,
        'asistencias': asistencias,
        'total_presentes': sum(1 for asistencia in asistencias if asistencia.present)
    }

    # Renderizar el template a HTML
    html = render_to_string('attendances/reporte_asistencias.html', context)

    # Crear un objeto de respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="asistencias_{curso.name}_{fecha}.pdf"'

    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}', status=500)
    return response