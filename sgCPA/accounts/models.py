from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os

# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True , null=True)


class Role(models.Model):
    ROLES= (
        ('admin', 'Administrador'),
        ('user', 'Usuario'),
    )
    name = models.CharField(max_length=5, choices=ROLES, default='user')
    description = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if not os.environ.get('ROLES_CREATED'):
        if not Role.objects.filter(name='admin').exists():
            Role.objects.create(name='admin', description='Administrador')

        if not Role.objects.filter(name='user').exists():
            Role.objects.create(name='user', description='Usuario')
        
        os.environ['ROLES_CREATED'] = 'True'

class UserRoles(models.Model):
    # only one role per user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} - {self.role}'


