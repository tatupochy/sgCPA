from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(null=True, default=True)