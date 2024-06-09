from django.db import models
from django.utils import timezone
from students.models import Course, Student

class Attendance(models.Model):
    date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # present = models.BooleanField()
    students = models.ManyToManyField(Student, through='AttendanceStudent')

    class Meta:
        permissions = [
            ('xyz_puede_ver_asistencias', 'Puede ver asistencias'),
            ('xyz_puede_crear_asistencias', 'Puede crear asistencias'),
            ('xyz_puede_modificar_asistencias', 'Puede modificar asistencias'),
            ('xyz_puede_eliminar_asistencias', 'Puede eliminar asistencias'),
        ]
        
class AttendanceStudent(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    present = models.BooleanField()
    
    
