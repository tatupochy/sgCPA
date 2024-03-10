from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    birthDate = models.DateField()
    inscriptionDate = models.DateField()
    ciNumber = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    fatherPhone = models.CharField(max_length=20)
    motherPhone = models.CharField(max_length=20)