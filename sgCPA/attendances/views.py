# attendances/views.py
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from students.models import Course, CourseDates,Student
from payments.models import Enrollment
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.http import HttpResponseBadRequest
from .models import Attendance, AttendanceStudent
# AttendanceRecord
from django.urls import reverse
from django.views.generic import DetailView
from django.urls import reverse_lazy
from collections import defaultdict
from .utils import check_attendance,calcular_asistencia_mes,get_business_days,get_business_days_in_month,get_expected_attendance_days
from calendar import monthrange, month_name
from datetime import datetime, timedelta, date
import calendar
from django.forms.models import model_to_dict
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import json



# sgCPA\attendances\views.py
def registrar_asistencia(request):
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')
        curso_id = request.POST['curso']
        curso = Course.objects.get(pk=curso_id)
        matriculaciones = Enrollment.objects.filter(course=curso)
        
        students = [matriculacion.student for matriculacion in matriculaciones]
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        
        existing_attendances = Attendance.objects.filter(date=fecha, course=curso)
        
        if existing_attendances.exists():
            # attendance = Attendance.objects.get(date=fecha, course=curso)
            return render(request, 'attendances/registrar_asistencia.html', {'message': 'registro de asistencia ya generado anteriormente'})
        # except ObjectDoesNotExist:
        
        attendance = Attendance.objects.create(date=fecha, course=curso)

        
        for student in students:
            presente = request.POST.get(str(student.id)) is not None
            AttendanceStudent.objects.create(attendance=attendance, student=student, present=presente)
    
        return render(request, 'attendances/registrar_asistencia.html', {'message': 'datos guardados correctamente'})
    else:
        now = timezone.now().date()
        cursos = Course.objects.filter(start_date__lte=now, end_date__gte=now)
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
        # if selected_mes:
        #     selected_mes = int(selected_mes)

        # if curso_id:
        #     selected_curso = Course.objects.get(pk=curso_id)
        #     enrollments = Enrollment.objects.filter(course=selected_curso).select_related('student')
        #     alumnos = [enrollment.student for enrollment in enrollments]
        #     asistencias = Attendance.objects.filter(course=selected_curso).order_by('date')

        #     # Obtener los meses del rango del curso
        #     start_month = selected_curso.start_date.month
        #     end_month = selected_curso.end_date.month
        #     meses_curso = [(m, month_name[m]) for m in range(start_month, end_month + 1)]

        #     # Excluir el mes actual
        #     current_year = date.today().year
        #     current_month = date.today().month
        #     if selected_mes and selected_mes <= current_month and selected_curso.end_date.year == current_year:
        #         asistencias = asistencias.filter(date__month=selected_mes)
        #     else:
        #         asistencias = asistencias.none()  # No mostrar asistencias si el mes es el actual o futuro

        #     for alumno in alumnos:
        #         for month in range(start_month, end_month + 1):
        #             # Calcular solo para meses anteriores al mes actual
        #             if month < current_month or selected_curso.end_date.year < current_year:
        #                 year = selected_curso.end_date.year
        #                 dias_por_semana = selected_curso.days_per_week
        #                 expected_classes = get_business_days_in_month(year, month, dias_por_semana)
        #                 asistencia_mes = calcular_asistencia_mes(alumno.id, month, selected_curso)
        #                 if asistencia_mes < 0.7 * expected_classes:
        #                     low_attendance_students[alumno.id].append(month)
    else:
        return render(request, 'attendances/listado_asistencias.html', {
            'cursos': cursos,
            # 'alumnos': alumnos,
            # 'asistencias': asistencias,
            # 'low_attendance_students': low_attendance_students,
            # 'meses_curso': meses_curso,
            # 'selected_curso': selected_curso,
            # 'selected_mes': selected_mes,
        })

def obtener_fechas_curso(request, curso_id):
    curso = get_object_or_404(Course, pk=curso_id)
    fechas = CourseDates.objects.filter(course=curso)
    fechas_formateadas = [fecha.date.strftime("%d/%m/%Y") for fecha in fechas]
        
    return JsonResponse({'fechas': fechas_formateadas})

def obtener_asistencias(request, id):
    body = json.loads(request.body)
    fecha_str = body.get('value')
    fecha = datetime.strptime(fecha_str, '%d/%m/%Y').date()
    
    course = get_object_or_404(Course, pk=id)
    
    try:    
        attendance = get_object_or_404(Attendance, course=course, date=fecha)
        
        
        alumnos_asistencias = attendance.attendancestudent_set.all()
        datos_asistencia = []
        for registro in alumnos_asistencias:
            alumno = registro.student
            nombre_alumno = alumno.name
            apellido = alumno.lastName
            ci = alumno.ciNumber
            presente = registro.present
            
            datos_alumno = {
                'nombre': nombre_alumno,
                'apellido': apellido,
                'presente': 'P' if registro.present else 'A',
                'ci':ci
            }
            datos_asistencia.append(datos_alumno)
    
        return JsonResponse({'asistencias': datos_asistencia})
    except:
        return JsonResponse({'asistencias': []})

def obtener_rango_curso(request, id):
   curso = get_object_or_404(Course, pk=id)
   curso_dict = model_to_dict(curso)
   fechas = curso.coursedates_set.all()
   fechas_formateadas = [fecha.date.strftime("%d/%m/%Y")  for fecha in fechas]
    
    # Convertir campos de fecha y hora a cadenas de texto
   for key, value in curso_dict.items():
        if isinstance(value, (date, datetime)):
            curso_dict[key] = value.isoformat()

    # Convertir objetos relacionados a sus identificadores
   for field in curso._meta.get_fields():
        if field.is_relation and field.many_to_one:
            related_obj = getattr(curso, field.name)
            if related_obj is not None:
                curso_dict[field.name] = related_obj.pk
                
   range = {'inicio': curso_dict['start_date'],
            'fin': curso_dict['end_date']}
   
                
   return JsonResponse({'rango':range, 'fechas': fechas_formateadas})

# def obtener_asistencia(request, )