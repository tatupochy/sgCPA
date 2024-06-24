# attendances/views.py
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from students.models import Course, CourseDates,Student
from payments.models import Enrollment, EnrollmentDetail
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
from xhtml2pdf import pisa
from django.template.loader import render_to_string



# sgCPA\attendances\views.py
def registrar_asistencia(request):
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')
        curso_id = request.POST['curso']
        curso = get_object_or_404(Course, pk=curso_id)
        
        # Obtener las matriculaciones activas del curso
        matriculaciones = Enrollment.objects.filter(course=curso, active=True)
        
        # Obtener los alumnos matriculados a través de los detalles de matriculación
        detalles_matriculaciones = EnrollmentDetail.objects.filter(enrollment__in=matriculaciones, active=True)
        
        students = [detalle.student for detalle in detalles_matriculaciones]
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        
        attendance = get_object_or_404(Attendance, date=fecha, course=curso)

        for student in students:
            presente = request.POST.get(str(student.id)) is not None
            AttendanceStudent.objects.filter(attendance=attendance, student=student).update(present=presente)
    
        return redirect(reverse('registrar_asistencia'))
    else:
        now = timezone.now().date()
        cursos = Course.objects.filter(start_date__lte=now, end_date__gte=now)
        return render(request, 'attendances/registrar_asistencia.html', {'cursos': cursos})

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
    try:
        # Parsear el cuerpo de la solicitud
        body = json.loads(request.body)
        fecha_str = body.get('value')
        fecha = datetime.strptime(fecha_str, '%d/%m/%Y').date()
        
        # Obtener el curso
        course = get_object_or_404(Course, pk=id)
        
        # Obtener la asistencia para el curso y la fecha especificados
        attendance = get_object_or_404(Attendance, course=course, date=fecha)
        
        # Obtener todas las relaciones AttendanceStudent para esta asistencia
        alumnos_asistencias = attendance.attendancestudent_set.all()
        datos_asistencia = []
        
        # Construir la lista de datos de asistencia para enviar como respuesta JSON
        for registro in alumnos_asistencias:
            alumno = registro.student
            datos_alumno = {
                'nombre': alumno.name,
                'apellido': alumno.lastName,
                'presente': 'P' if registro.present else 'A' if registro.present is False else 'Indefinido',
                'ci': alumno.ciNumber,
                'id_alumno': alumno.id
            }
            datos_asistencia.append(datos_alumno)
        
        # Retornar la respuesta JSON con los datos de asistencia
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

#PDF
def descargar_asistencias_pdf(request):
    body = json.loads(request.body)
    curso_id = body.get('curso_id')
    fecha_str = body.get('fecha')
    curso = get_object_or_404(Course, pk=curso_id)
    profesor = curso.teacher.name + " " + curso.teacher.lastName
  
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()  # Cambiado a '%d/%m/%Y'
    except ValueError:
        return HttpResponse("Formato de fecha incorrecto", status=400)
    
    
    print(fecha)
    print(curso)
    
    attendance = get_object_or_404(Attendance, course=curso, date=fecha)
    asistencias = attendance.attendancestudent_set.all()
    
    # Preparar el contexto para el template
    context = {
        'curso': curso,
        'fecha': fecha,
        'asistencias': asistencias,
        'profesor':profesor,
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



###################################################################
def registrar_asistencia2(request):
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')
        curso_id = request.POST['curso']
        curso = get_object_or_404(Course, pk=curso_id)
        
        # Obtener las matriculaciones activas del curso
        matriculaciones = Enrollment.objects.filter(course=curso, active=True)
        
        # Obtener los alumnos matriculados a través de los detalles de matriculación
        detalles_matriculaciones = EnrollmentDetail.objects.filter(enrollment__in=matriculaciones, active=True)
        
        students = [detalle.student for detalle in detalles_matriculaciones]
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        
        attendance = get_object_or_404(Attendance, date=fecha, course=curso)

        for student in students:
            presente = request.POST.get(str(student.id)) is not None
            AttendanceStudent.objects.filter(attendance=attendance, student=student).update(present=presente)
    
        return redirect(reverse('registrar_asistencia2'))
    else:
        now = timezone.now().date()
        cursos = Course.objects.filter(start_date__lte=now, end_date__gte=now)
        return render(request, 'attendances/registrar_asistencia2.html', {'cursos': cursos})

def obtener_fechas_curso2(request, curso_id):
    curso = get_object_or_404(Course, pk=curso_id)
    fechas = CourseDates.objects.filter(course=curso)
    today = timezone.now().date()

    #prueba
    #today = datetime.strptime("2024-06-22", "%Y-%m-%d").date()

    # # # Debug: Imprimir fechas y fecha actual
    # print("Curso ID:", curso_id)
    # print("Fechas del curso:", [fecha.date for fecha in fechas])
    # print("Fecha actual:", today)

    # Comprobar si alguna fecha del curso coincide con la fecha actual
    fecha_hoy_en_curso = any(fecha.date == today for fecha in fechas)
    # print("Fecha hoy en curso:", fecha_hoy_en_curso)
    if fecha_hoy_en_curso:
        return JsonResponse({'fecha': today.strftime("%d/%m/%Y")})
    else:
        return JsonResponse({'fecha': None})
    