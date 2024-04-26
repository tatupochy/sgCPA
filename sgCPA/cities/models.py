from django.db import models

from countries.models import Country

# Create your models here.
class Cities(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(null=True, default=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
