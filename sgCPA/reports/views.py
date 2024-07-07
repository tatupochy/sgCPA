from django.shortcuts import render
from django.db.models import Count,Min
from django.db.models.functions import TruncMonth
from attendances.models import AttendanceStudent
from students.models import Course
import calendar
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import datetime

import json


# Create your views here.
def reports(request):
    return render(request, 'reports.html')

def report_cursos_mas_ausencias(request):
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    # Meses en español
    months = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]

    # Calcular el rango de años basado en start_date
    min_start_date = Course.objects.aggregate(min_start_date=Min('start_date'))['min_start_date']
    current_year = datetime.datetime.now().year
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
    attendance_months_dict = {date.strftime('%Y-%m'): date.strftime('%B') for date in attendance_months}
    translated_months = {calendar.month_name[i]: months[i-1] for i in range(1, 13)}
    attendance_months_translated = {k: translated_months[v] for k, v in attendance_months_dict.items()}

    filter_args = {'present': False}
    if selected_month and selected_year:
        month_number = list(translated_months.values()).index(selected_month) + 1
        filter_args['attendance__date__month'] = month_number
        filter_args['attendance__date__year'] = selected_year

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
        'months': list(attendance_months_translated.values()),
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


def download_pdf_report(request):
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

    current_time = datetime.datetime.now()
    context = {
        'data': ausencias,
        'current_date': current_time.strftime("%Y-%m-%d"),
        'current_time': current_time.strftime("%H:%M:%S")
    }

    # Renderizar la plantilla HTML
    html_string = render_to_string('report_pdf_template.html', context)

    # Crear un objeto de respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_cursos_mas_ausencias_{current_time.strftime("%Y-%m-%d")}.pdf"'

    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}', status=500)
    return response