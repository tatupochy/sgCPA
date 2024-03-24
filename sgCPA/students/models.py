from django.db import models

# Create your models here.


###### Cursos disponibles ######
class Course(models.Model):
    CHOICE_SHIFTS = [
        ('M', 'Mañana'),
        ('T', 'Tarde'),
        ('S', 'Sábado'),
    ]

    CHOICES_SECTIONS = [
        ('1', '1'),
        ('2', '2'),
    ]

    name = models.CharField(max_length=100)
    shift = models.CharField(max_length=1, choices=CHOICE_SHIFTS)
    section = models.CharField(max_length=1, choices=CHOICES_SECTIONS, blank=True)
    active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    fee_amount = models.DecimalField(max_digits=10, decimal_places=0)
    days_per_week = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        if self.section:
            return f"{self.name} - {self.get_shift_display()} {self.section}"
        else:
            return f"{self.name} - {self.get_shift_display()}"
        
class Student(models.Model):
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, default=None)
    birthDate = models.DateField()
    inscriptionDate = models.DateField()
    ciNumber = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    fatherPhone = models.CharField(max_length=20)
    motherPhone = models.CharField(max_length=20)
    active = models.BooleanField(null=True, default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)