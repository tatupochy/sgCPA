import locale
from django.shortcuts import render
from django.db.models import Count,Min, Sum, Q
from django.db.models.functions import TruncMonth,ExtractYear, ExtractMonth
from attendances.models import AttendanceStudent
from students.models import Course, Shift
import calendar
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.utils import timezone
from collections import defaultdict
import json
from payments.models import EnrollmentDetail, Fee, Payment
from constans.paymentStates import StateEnum
from students.models import Course, Student
from django.db.models import Count
from dateutil.relativedelta import relativedelta
# from io import BytesIO
# from PyPDF2 import PdfReader
# Create your views here.

#Menu principal
def reports(request):
    return render(request, 'reports.html')

def report_cursos_mas_ausencias(request):
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    # Meses en español
    months = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    month_lookup = {i: month for i, month in enumerate(months, 1)}

    # Calcular el rango de años basado en start_date
    min_start_date = Course.objects.aggregate(min_start_date=Min('start_date'))['min_start_date']
    current_year = datetime.now().year
    years = list(range(min_start_date.year, current_year + 1))

    # Filtrar solo los meses y años con asistencias registradas
    attendance_months = AttendanceStudent.objects.values(
        month=TruncMonth('attendance__date')
    ).annotate(
        count=Count('id')
    ).values_list(
        'month', flat=True
    ).distinct()

    # Convertir las fechas de los meses a nombres de meses en español y años
    unique_months = sorted(set((date.year, date.month) for date in attendance_months))
    attendance_months_translated = [month_lookup[month] for year, month in unique_months]

    filter_args = {'present': False}
    if selected_month and selected_year:
        month_number = months.index(selected_month) + 1
        filter_args['attendance__date__month'] = month_number
        filter_args['attendance__date__year'] = int(selected_year)

    data = AttendanceStudent.objects.filter(**filter_args).values(
        'attendance__course__name',
        year=TruncMonth('attendance__date')
    ).annotate(
        total_ausencias=Count('id')
    ).order_by('-total_ausencias')

    chart_data = {}
    for entry in data:
        year_month = entry['year'].strftime('%Y-%m')
        course_name = entry['attendance__course__name']
        total_ausencias = entry['total_ausencias']

        if year_month not in chart_data:
            chart_data[year_month] = {}

        chart_data[year_month][course_name] = total_ausencias

    labels = list(chart_data.keys())
    courses = list(set(course for month_data in chart_data.values() for course in month_data))
    dataset = [
        {
            'label': course,
            'data': [chart_data[month].get(course, 0) for month in labels]
        }
        for course in courses
    ]

    return render(request, 'report_cursos_mas_ausencias.html', {
        'data': data,
        'labels': labels,
        'dataset': dataset,
        'months': attendance_months_translated,
        'years': years,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'no_data': not data.exists()
    })

def report_cursos_mas_presentes(request):
    data = AttendanceStudent.objects.filter(present=True).values(
        'attendance__course__name',
        year=TruncMonth('attendance__date')
    ).annotate(
        total_presentes=Count('id')
    ).order_by('-total_presentes')

    chart_data = {}
    for entry in data:
        year_month = entry['year'].strftime('%Y-%m')
        course_name = entry['attendance__course__name']
        total_presentes = entry['total_presentes']

        if year_month not in chart_data:
            chart_data[year_month] = {}

        chart_data[year_month][course_name] = total_presentes

    labels = list(chart_data.keys())
    courses = list(set(course for month_data in chart_data.values() for course in month_data))
    dataset = [
        {
            'label': course,
            'data': [chart_data[month].get(course, 0) for month in labels]
        }
        for course in courses
    ]

    return render(request, 'report_cursos_mas_presentes.html', {
        'data': data,
        'labels': labels,
        'dataset': dataset
    })

# #reporte de asistencias

# def download_pdf_report(request):
    body = json.loads(request.body)
    month = body.get('month')
    year = body.get('year')

    # Filtrar datos según los valores de month y year, si están vacíos, traer todos los datos
    ausencias = AttendanceStudent.objects.filter(present=False)
    if month:
        ausencias = ausencias.filter(attendance__date__month=month)
    if year:
        ausencias = ausencias.filter(attendance__date__year=year)
    
    ausencias = ausencias.values('attendance__course__name', 'attendance__date__month', 'attendance__date__year') \
                        .annotate(total_ausencias=Count('id')).order_by('-total_ausencias')

    current_time = datetime.now()
    context = {
        'data': ausencias,
        'current_date': current_time.strftime("%Y-%m-%d"),
        'current_time': current_time.strftime("%H:%M:%S"),
        'page_number': '',  # Placeholder for page number
        'total_pages': ''   # Placeholder for total pages
    }

    # Renderizar la plantilla HTML sin paginación para contar las páginas
    html_string = render_to_string('report_pdf_template.html', context)
    
    # Convertir HTML a PDF sin paginación para contar páginas
    # result = BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=result)
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}', status=500)
    
    # Contar el número total de páginas
    pdf_content = result.getvalue()
    total_pages = pdf_content.count(b'/Page')
    result.seek(0)

    # Renderizar HTML con paginación real
    context['total_pages'] = total_pages
    paginated_html_string = render_to_string('report_pdf_template.html', context)
    # result = BytesIO()
    pisa_status = pisa.CreatePDF(paginated_html_string, dest=result)
    
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}', status=500)
    
    # Crear un objeto de respuesta PDF
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_cursos_mas_ausencias_{current_time.strftime("%Y-%m-%d")}.pdf"'

    return response

#     # Renderizar la plantilla HTML
#     html_string = render_to_string('report_pdf_template.html', context)

#     # Crear un objeto de respuesta PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="reporte_cursos_mas_ausencias_{current_time.strftime("%Y-%m-%d")}.pdf"'

#     # Convertir HTML a PDF
#     pisa_status = pisa.CreatePDF(html_string, dest=response)
#     if pisa_status.err:
#         return HttpResponse(f'Error al generar el PDF: {pisa_status.err}', status=500)
#     return response

#Morosidad
def latePayments(request, year=None, month=None):
    students = Student.objects.all()
    studentsDebts = []

    # Definir el rango de fechas si se proporcionan month y year
    if month and year:
        start_date = datetime(year, month, 1)
        end_date = start_date + relativedelta(months=1) - timedelta(days=1)
    else:
        start_date = None
        end_date = None

    # Obtener el año actual
    current_year = timezone.now().year

    # Obtener el menor año con cuotas vencidas hasta el año actual en la tabla Fee
    earliest_overdue_year_fee = Fee.objects.filter(
        state__name=StateEnum.Vencido.value,
        expiration_date__year__lte=current_year
    ).aggregate(earliest_year=Min('expiration_date__year'))['earliest_year']

    # Generar la lista de años desde el menor año con cuotas vencidas hasta el año actual
    if earliest_overdue_year_fee:
        years_range = list(range(earliest_overdue_year_fee, current_year + 1))
    else:
        years_range = []

    for student in students:
        
        studentFees = Fee.objects.filter(student=student)
        
        # Sumar cuotas de tarifas vencidas
        if start_date and end_date:
            studentOverdueFees = studentFees.filter(
                state__name=StateEnum.Vencido.value,
                expiration_date__range=(start_date, end_date)
            ).aggregate(total_amount=Sum('fee_amount'))['total_amount'] or 0
        else:
            studentOverdueFees = studentFees.filter(
                state__name=StateEnum.Vencido.value
            ).aggregate(total_amount=Sum('fee_amount'))['total_amount'] or 0
        
        # Encontrar la fecha de la cuota más antigua que esté vencida
        if start_date and end_date:
            oldest_overdue_fee_date = studentFees.filter(
                state__name=StateEnum.Vencido.value,
                expiration_date__range=(start_date, end_date)
            ).aggregate(Min('expiration_date'))['expiration_date__min']
        else:
            oldest_overdue_fee_date = studentFees.filter(
                state__name=StateEnum.Vencido.value
            ).aggregate(Min('expiration_date'))['expiration_date__min']
        
        if oldest_overdue_fee_date:
            current_date = timezone.now().date()
            days_overdue = (current_date - oldest_overdue_fee_date).days
            days_overdue_interval = (days_overdue // 30) * 30
        else:
            days_overdue_interval = 0
        
        totalDebt = studentOverdueFees

        if totalDebt > 0:
            studentsDebts.append({
                'totalDebt': totalDebt,
                'name': student.name,
                'ciNumber': student.ciNumber,
                'atraso': days_overdue_interval
            })
    
    studentsDebts_sorted = sorted(studentsDebts, key=lambda x: x['totalDebt'], reverse=True)
    
    if month and year:
        data = {
            'studentsDebts': studentsDebts_sorted
        }
        return JsonResponse(data)    
    else:    
        return render(request, 'latePayments.html', {
            'studentsDebts': studentsDebts_sorted,
            'years_range': years_range,
            'selected_year': year,
            'selected_month': str(month) if month else None
        })


def coursesRanking(request, year=None, month=None):
    
     # Filtrar EnrollmentDetail por año y mes si se proporcionan
    enrollment_details = EnrollmentDetail.objects.all()
    if year:
        enrollment_details = enrollment_details.filter(student_enrollment_date__year=year)
    if year and month:
        enrollment_details = enrollment_details.filter(student_enrollment_date__year=year, student_enrollment_date__month=month)

        
     # Obtener el primer año de registros y el año actual
    first_enrollment = EnrollmentDetail.objects.aggregate(first_year=Min('student_enrollment_date'))
    first_year = first_enrollment['first_year'].year if first_enrollment['first_year'] else datetime.datetime.now().year
    
    current_year = datetime.now().year
    years = list(range(first_year, current_year + 1))

    courses_with_enrollment_counts = Course.objects.annotate(num_enrollment_details=Count('enrollment__enrollmentdetail')).filter(num_enrollment_details__gt=0).order_by('-num_enrollment_details')
    
    shifts = Shift.objects.all()
    
    courses_list = []
    for course in courses_with_enrollment_counts:
        courses_list.append({
            'course_name': course.name,
            'num_enrollment_details': course.num_enrollment_details,
            'shift': course.shift
        })

    data = {
        'courses_list': courses_list,
        'shifts': shifts,
        'years': years
    }

    return render(request, 'coursesRanking.html', data)

def get_courses_ranking_filter(request, year=None, month=None, shift_id=None):
     # Filtrar EnrollmentDetail por año y mes si se proporcionan
    filter_criteria = Q()
    if year:
        filter_criteria &= Q(enrollment__enrollmentdetail__student_enrollment_date__year=year)
    if month:
        filter_criteria &= Q(enrollment__enrollmentdetail__student_enrollment_date__month=month)

    # Construir un filtro para Shift basado en el parámetro shift_id
    shift_filter = Q()
    if shift_id:
        shift_filter &= Q(shift_id=shift_id)

    # Anotar los cursos con el número de detalles de inscripción que cumplen con el filtro
    courses_with_enrollment_counts = Course.objects.annotate(
        num_enrollment_details=Count('enrollment__enrollmentdetail', filter=filter_criteria)
    ).filter(
        num_enrollment_details__gt=0
    ).filter(
        shift_filter
    ).order_by('-num_enrollment_details')
        
    shifts = Shift.objects.all()
    shifts_list = [{'id': shift.id, 'name': shift.name} for shift in shifts]
    
    courses_list = []
    for course in courses_with_enrollment_counts:
        courses_list.append({
            'course_name': course.name,
            'num_enrollment_details': course.num_enrollment_details,
            'shift':  {'id': course.shift.id, 'name': course.shift.name} if course.shift else None
        })

    data = {
        'courses_list': courses_list,
        'shifts': shifts_list
    }
    
    return JsonResponse(data)

def revenues(request):
    
    
    min_year = Course.objects.aggregate(Min('year'))['year__min']
    
    current_year = datetime.now().year
    
    years = list(range(min_year, current_year + 1))

    data = {
        'years': years
    }

    return render(request, 'revenues.html', data)

def get_revenues_per_year(request, year, month=None):
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Diccionario de equivalentes de meses en letras y en español
    months_in_spanish = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    # Filtrar pagos por año
    if month:
        # Si se proporciona un mes, filtrar por año y mes
        total_revenue = Payment.objects.filter(year=year, payment_date__month=month).aggregate(total=Sum('payment_amount'))['total']
        if total_revenue is None:
            total_revenue = 0

        # Formatear el total mensual con separadores de miles y sin decimales
        formatted_total_revenue = int(total_revenue)

        # Contar los cursos activos por mes
        active_courses_count = Course.objects.filter(
            active=True, 
            start_date__year=year, 
            start_date__month__lte=month, 
            end_date__month__gte=month
        ).count()
        
        # Crear un diccionario para almacenar las ganancias mensuales y cursos activos
        monthly_revenues_dict = {month: {"revenue": formatted_total_revenue, "active_courses": active_courses_count}}
    else:
        # Filtrar pagos por año y calcular el total anual
        total_revenue = Payment.objects.filter(year=year).aggregate(total=Sum('payment_amount'))['total']
        if total_revenue is None:
            total_revenue = 0

        # Formatear el total anual con separadores de miles y sin decimales
        formatted_total_revenue = int(total_revenue)

        # Filtrar pagos por año y mes y calcular los totales mensuales
        monthly_revenues = Payment.objects.filter(year=year).values('payment_date__month').annotate(total=Sum('payment_amount'))

        # Crear un diccionario para almacenar las ganancias mensuales y cursos activos
        monthly_revenues_dict = {month: {"revenue": 0, "active_courses": 0} for month in range(1, 13)}
        for revenue in monthly_revenues:
            month = revenue['payment_date__month']
            total = revenue['total']
            monthly_revenues_dict[month]["revenue"] = int(total)

        # Limitar los datos hasta el mes actual si el año es el actual
        if year == current_year:
            monthly_revenues_dict = {month: data for month, data in monthly_revenues_dict.items() if month <= current_month}

        # Contar los cursos activos por mes
        for month in range(1, 13):
            if year == current_year and month > current_month:
                break
            active_courses_count = Course.objects.filter(
                active=True, 
                start_date__year=year, 
                start_date__month__lte=month, 
                end_date__month__gte=month
            ).count()
            monthly_revenues_dict[month]["active_courses"] = active_courses_count

    # Formatear las ganancias mensuales y cambiar los meses a letras en español
    formatted_monthly_revenues = [
        {"month": months_in_spanish[month], "revenue": data["revenue"], "active_courses": data["active_courses"]}
        for month, data in monthly_revenues_dict.items()
    ]

    return JsonResponse({
        "year": year,
        "total_revenue": formatted_total_revenue,
        "monthly_revenues": formatted_monthly_revenues
    })

#############################################
# Alumnos matriculados por anho
#############################################

def reporte_matriculas(request):
    enrollments = EnrollmentDetail.objects.all()
    data = defaultdict(int)
    
    for enrollment in enrollments:
        year = enrollment.student_enrollment_date.year
        data[year] += 1
    
    total_general = sum(data.values())
    
    context = {
        'data': dict(data),
        'total_general': total_general,
        'fecha': timezone.now().date(),
        'hora': timezone.now().time(),
        'years': list(data.keys()),  # Pasar los años disponibles al contexto
        'selected_year': request.GET.get('year', '')  # Mantener el año seleccionado en el filtro
    }
    
    return render(request, 'reporte_matriculas.html', context)


def download_pdf_report_matriculados_anho(request):
    body = json.loads(request.body)
    year = body.get('year')

    # Filtrar datos según el valor de year, si está vacío, traer todos los datos
    matriculas = EnrollmentDetail.objects.all()
    if year:
        matriculas = matriculas.filter(student_enrollment_date__year=year)

    matriculas = matriculas.annotate(
        year=ExtractYear('student_enrollment_date'),
        month=ExtractMonth('student_enrollment_date')
    ).values('year', 'month').annotate(total_matriculas=Count('id')).order_by('year', 'month')

    current_time = datetime.now()
    context = {
        'data': matriculas,
        'current_date': current_time.strftime("%Y-%m-%d"),
        'current_time': current_time.strftime("%H:%M:%S")
    }

    # Renderizar la plantilla HTML
    html_string = render_to_string('report_pdf_matriculados_anho.html', context)

    # Crear un objeto de respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_matriculas_{current_time.strftime("%Y-%m-%d")}.pdf"'

    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}', status=500)
    return response

#prueba
# def download_pdf_report(request):
    body = json.loads(request.body)
    month = body.get('month')
    year = body.get('year')

    # Filtrar datos según los valores de month y year, si están vacíos, traer todos los datos
    ausencias = AttendanceStudent.objects.filter(present=False)
    if month:
        ausencias = ausencias.filter(attendance__date__month=month)
    if year:
        ausencias = ausencias.filter(attendance__date__year=year)
    
    ausencias = ausencias.values('attendance__course__name', 'attendance__date__month', 'attendance__date__year') \
                        .annotate(total_ausencias=Count('id')).order_by('-total_ausencias')

    current_time = datetime.now()
    context = {
        'data': ausencias,
        'current_date': current_time.strftime("%Y-%m-%d"),
        'current_time': current_time.strftime("%H:%M:%S"),
        'page_number': '',  # Placeholder for page number
        'total_pages': ''   # Placeholder for total pages
    }

    # Renderizar la plantilla HTML
    html_string = render_to_string('report_pdf_template.html', context)
    
    # Convertir HTML a PDF para contar las páginas
    result = BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=result)
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}', status=500)
    
    # Contar el número total de páginas usando PdfReader
    result.seek(0)
    pdf_reader = PdfReader(result)
    total_pages = len(pdf_reader.pages)
    result.seek(0)

    # Renderizar HTML con paginación real
    context['total_pages'] = total_pages
    paginated_html_string = render_to_string('report_pdf_template.html', context)
    result = BytesIO()
    pisa_status = pisa.CreatePDF(paginated_html_string, dest=result)
    
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}', status=500)
    
    # Crear un objeto de respuesta PDF
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_cursos_mas_ausencias_{current_time.strftime("%Y-%m-%d")}.pdf"'

    return response