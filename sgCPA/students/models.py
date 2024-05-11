from django.db import models

from cities.models import Cities
from countries.models import Country
from subjects.models import Subject

# Create your models here.


###### Cursos disponibles ######
class Course(models.Model):

    name = models.CharField(max_length=100)
    shift = models.ForeignKey('Shift', on_delete=models.CASCADE)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    fee_amount = models.DecimalField(max_digits=10, decimal_places=0)
    days_per_week = models.IntegerField()
    year = models.IntegerField()
    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        if self.section:
            return f"{self.name} - {self.get_shift_display()} {self.section}"
        else:
            return f"{self.name} - {self.get_shift_display()}"
        
    class Meta:
        permissions = [
            ('xyz_puede_ver_cursos', 'Puede ver cursos'),
            ('xyz_puede_crear_cursos', 'Puede crear cursos'),
            ('xyz_puede_modificar_cursos', 'Puede modificar cursos'),
            ('xyz_puede_eliminar_cursos', 'Puede eliminar cursos'),
        ]


class Shift(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ('xyz_puede_ver_turnos', 'Puede ver turnos'),
            ('xyz_puede_crear_turnos', 'Puede crear turnos'),
            ('xyz_puede_modificar_turnos', 'Puede modificar turnos'),
            ('xyz_puede_eliminar_turnos', 'Puede eliminar turnos'),
        ]


class Section(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ('xyz_puede_ver_secciones', 'Puede ver secciones'),
            ('xyz_puede_crear_secciones', 'Puede crear secciones'),
            ('xyz_puede_modificar_secciones', 'Puede modificar secciones'),
            ('xyz_puede_eliminar_secciones', 'Puede eliminar secciones'),
        ]

        
class Student(models.Model):
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, default=None)
    birthDate = models.DateField()
    ciNumber = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    fatherPhone = models.CharField(max_length=20)
    motherPhone = models.CharField(max_length=20)
    active = models.BooleanField(null=True, default=True)
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    class Meta:
        permissions = [
            ('xyz_puede_ver_estudiantes', 'Puede ver estudiantes'),
            ('xyz_puede_crear_estudiantes', 'Puede crear estudiantes'),
            ('xyz_puede_modificar_estudiantes', 'Puede modificar estudiantes'),
            ('xyz_puede_eliminar_estudiantes', 'Puede eliminar estudiantes'),
        ]
