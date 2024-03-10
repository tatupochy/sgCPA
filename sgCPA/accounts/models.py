from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Role(models.Model):
    ROLES= (
        ('admin', 'Administrador'),
        ('user', 'Usuario'),
    )
    name = models.CharField(max_length=5, choices=ROLES, default='user')
    description = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name


class UserRoles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} - {self.role}'


