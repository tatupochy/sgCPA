from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(null=True, default=True)

    class Meta:
        permissions = [
            ('xyz_puede_ver_materias', 'Puede ver materias'),
            ('xyz_puede_crear_materias', 'Puede crear materias'),
            ('xyz_puede_modificar_materias', 'Puede modificar materias'),
            ('xyz_puede_eliminar_materias', 'Puede eliminar materias'),
        ]