import os
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_migrate

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

    class Meta:
        permissions = [
            ('xyz_puede_ver_personas', 'Puede ver personas'),
            ('xyz_puede_agregar_personas', 'Puede agregar personas'),
            ('xyz_puede_modificar_personas', 'Puede modificar personas'),
            ('xyz_puede_eliminar_personas', 'Puede eliminar personas'),
        ]
        

class UserLogin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True)
    last_logout = models.DateTimeField(auto_now=True)
    attempts = models.IntegerField(default=0)


# class Role(models.Model):
#     ROLES= (
#         ('admin', 'Administrador'),
#         ('user', 'Usuario'),
#     )
#     name = models.CharField(max_length=5, choices=ROLES, default='user')
#     description = models.CharField(max_length=100, blank=True, null=True)
    
#     def __str__(self):
#         return self.name

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if not os.environ.get('GROUPS_CREATED'):
        if not Group.objects.filter(name='Administrador').exists():
            Group.objects.create(name='Administrador')

        if not Group.objects.filter(name='Usuario').exists():
            Group.objects.create(name='Usuario')
        
        os.environ['GROUPS_CREATED'] = 'True'

    # if user is superuser, add to admin group
    if User.objects.filter(is_superuser=True).exists():
        user = User.objects.get(is_superuser=True)
        admin_group = Group.objects.get(name='Administrador')
        user.groups.add(admin_group)
        user.save()

# class UserRoles(models.Model):
#     # only one role per user
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f'{self.user} - {self.role}'


