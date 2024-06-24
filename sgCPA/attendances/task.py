# attendances/tasks.py
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from students.models import Student
from .models import Attendance, AttendanceStudent, AttendanceSettings
import datetime

@shared_task
def check_absences_and_send_emails():
    try:
        # Verificar configuración de envío automático
        settings = AttendanceSettings.objects.first()
        if settings and not settings.automatic_email:
            return "El envío automático de correos está desactivado."

        students_with_absences = {}
        today = timezone.now().date()
        start_date = today - datetime.timedelta(days=30)  # Ajusta el período según sea necesario
        
        # Obtén las asistencias dentro del período
        attendances = Attendance.objects.filter(date__range=(start_date, today)).order_by('date')
        
        # Crea un diccionario para rastrear las ausencias consecutivas de cada estudiante
        student_absences = {}

        for attendance in attendances:
            for att_student in AttendanceStudent.objects.filter(attendance=attendance):
                if att_student.student_id not in student_absences:
                    student_absences[att_student.student_id] = 0

                if att_student.present:
                    student_absences[att_student.student_id] = 0
                else:
                    student_absences[att_student.student_id] += 1

                if student_absences[att_student.student_id] >= 5:
                    students_with_absences[att_student.student_id] = student_absences[att_student.student_id]
        
        for student_id in students_with_absences:
            student = Student.objects.get(id=student_id)
            subject = "Alerta de ausencias consecutivas"
            message = f"Estimado {student.name}, ha acumulado {students_with_absences[student_id]} ausencias consecutivas. Por favor, contacte a su docente."
            send_mail(subject, message, None, [student.email])

        return "Proceso de verificación de ausencias completado"

    except Exception as e:
        return f"Error al procesar ausencias: {str(e)}"
