# sgCPA\teachers\models.py
from django.db import models
from cities.models import Cities
from countries.models import Country

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, default=None)
    birthDate = models.DateField()
    ciNumber = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    active = models.BooleanField(null=True, default=True)
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)   
 
    def __str__(self):
        return self.name
    