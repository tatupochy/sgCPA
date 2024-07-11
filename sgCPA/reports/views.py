import locale
from django.shortcuts import render
from django.db.models import Count,Min, Sum
from django.db.models.functions import TruncMonth
from attendances.models import AttendanceStudent
from students.models import Course
import calendar
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa



import json


from payments.models import EnrollmentDetail, Fee, Payment
from constans.paymentStates import StateEnum
from students.models import Course, Student
from django.db.models import Count

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

#Morosidad
def latePayments(request):
    students = Student.objects.all()
    studentsDebts = []
    for student in students:
        studentEnrollments = EnrollmentDetail.objects.filter(student=student)
        
        enrollmentsOverdueAmount = sum(
            enrollment.enrollment_amount for enrollment in studentEnrollments if enrollment.state.name == StateEnum.Vencido.value
        )
        
        studentFees = Fee.objects.filter(student=student)
                
        studentOverdueFees = sum(
            fee.fee_amount for fee in studentFees if fee.state.name == StateEnum.Vencido.value
        )

        print(studentOverdueFees)
        
        totalDebt = enrollmentsOverdueAmount + studentOverdueFees

        studentDebts = {
            'totalDebt': totalDebt,
            'name': student.name,
            'ciNumber': student.ciNumber
        }

        if totalDebt > 0: 
            studentsDebts.append(studentDebts)
            
        studentsDebts_sorted = sorted(studentsDebts, key=lambda x: x['totalDebt'], reverse=True)
        
    return render(request, 'latePayments.html', {'studentsDebts': studentsDebts_sorted})


def coursesRanking(request):

    courses_with_enrollment_counts = Course.objects.annotate(num_enrollment_details=Count('enrollment__enrollmentdetail')).order_by('-num_enrollment_details')

    courses_list = []
    for course in courses_with_enrollment_counts:
        courses_list.append({
            'course_name': course.name,
            'num_enrollment_details': course.num_enrollment_details,
        })


    return render(request, 'coursesRanking.html', {'courses_list': courses_list})


def revenues(request):
    
    
    min_year = Course.objects.aggregate(Min('year'))['year__min']
    
    current_year = datetime.now().year
    
    years = list(range(min_year, current_year + 1))

    data = {
        'years': years
    }

    return render(request, 'revenues.html', data)


# def get_revenues_per_year(request, year):

#     # Filtrar los pagos por el año especificado y sumar el monto de los pagos
#     total_revenue = Payment.objects.filter(year=year).aggregate(total=Sum('payment_amount'))['total']

#     # Formatear el total de ingresos con separadores de miles
#     formatted_total_revenue = "{:,.0f}".format(total_revenue).replace(",", ".")


#     return JsonResponse({"year": year, "total_revenue": formatted_total_revenue})

def get_revenues_per_year(request, year):
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Diccionario de equivalentes de meses en letras y en español
    months_in_spanish = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    # Filtrar pagos por año y calcular el total anual
    total_revenue = Payment.objects.filter(year=year).aggregate(total=Sum('payment_amount'))['total']
    if total_revenue is None:
        total_revenue = 0

    # Formatear el total anual con separadores de miles y sin decimales
    formatted_total_revenue = int(total_revenue)

    # Filtrar pagos por año y mes y calcular los totales mensuales
    monthly_revenues = Payment.objects.filter(year=year).values('payment_date__month').annotate(total=Sum('payment_amount'))

    # Crear un diccionario para almacenar las ganancias mensuales
    monthly_revenues_dict = {month: 0 for month in range(1, 13)}
    for revenue in monthly_revenues:
        month = revenue['payment_date__month']
        total = revenue['total']
        monthly_revenues_dict[month] = int(total)

    # Limitar los datos hasta el mes actual si el año es el actual
    if year == current_year:
        monthly_revenues_dict = {month: total for month, total in monthly_revenues_dict.items() if month <= current_month}

    # Formatear las ganancias mensuales y cambiar los meses a letras en español
    formatted_monthly_revenues = [(months_in_spanish[month], total) for month, total in monthly_revenues_dict.items()]

    return JsonResponse({
        "year": year,
        "total_revenue": formatted_total_revenue,
        "monthly_revenues": formatted_monthly_revenues
    })