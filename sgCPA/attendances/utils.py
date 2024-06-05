from datetime import date, timedelta
from .models import Attendance
from payments.models import Enrollment  
from calendar import monthrange

def get_business_days(start_date, end_date):
    total_days = (end_date - start_date).days + 1
    business_days = 0

    for day in range(total_days):
        current_day = start_date + timedelta(days=day)
        if current_day.weekday() < 5:  # Lunes a Viernes
            business_days += 1

    return business_days

def get_expected_attendance_days(course):
    start_date = course.start_date
    end_date = min(course.end_date, date.today())
    total_days = (end_date - start_date).days + 1
    total_weeks = total_days // 7
    remaining_days = total_days % 7

    expected_days = total_weeks * course.days_per_week

    for day in range(remaining_days):
        current_day = start_date + timedelta(days=(total_weeks * 7) + day)
        if current_day.weekday() < 5:  # Lunes a Viernes
            expected_days += 1 / (5 / course.days_per_week)  # Ajustar la proporción de días hábiles

    return expected_days

def check_attendance(course):
    expected_days = get_expected_attendance_days(course)
    if expected_days == 0:
        return []

    threshold = expected_days * 0.7
    low_attendance_students = []

    enrollments = Enrollment.objects.filter(course=course)

    for enrollment in enrollments:
        attended_days = Attendance.objects.filter(student=enrollment.student, course=course, present=True).count()
        if attended_days < threshold:
            low_attendance_students.append({
                'student': enrollment.student,
                'attended_days': attended_days,
                'attendance_percentage': (attended_days / expected_days) * 100
            })

    return low_attendance_students

def calcular_asistencia_mes(alumno_id, mes, curso):
    asistencias_alumno_mes = Attendance.objects.filter(
        student_id=alumno_id,
        date__month=mes,
        course=curso
    )
    asistencias_totales_mes = asistencias_alumno_mes.count()
    return asistencias_totales_mes

def get_business_days_in_month(year, month, dias_por_semana):
    _, days_in_month = monthrange(year, month)
    total_weeks = days_in_month // 7
    remaining_days = days_in_month % 7
    total_business_days = total_weeks * dias_por_semana
    if remaining_days:
        # Ajustar para considerar semanas con menos días hábiles que la cantidad especificada
        total_business_days += min(remaining_days, dias_por_semana)
    return total_business_days
