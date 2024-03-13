from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os

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


