from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from students.models import Student, Course

# Create your models here.

class State(models.Model):
    STATE_CHOICES = (
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('overdue', 'Vencido'),
    )

    name = models.CharField(max_length=20, choices=STATE_CHOICES, default='pending')
    description = models.CharField(max_length=100, blank=True, null=True)

@receiver(post_migrate)
def create_state(sender, **kwargs):
    if sender.name == 'payments':
        State.objects.get_or_create(name='pending', description='Pendiente')
        State.objects.get_or_create(name='paid', description='Pagado')
        State.objects.get_or_create(name='overdue', description='Vencido')
    

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField()
    fee_date = models.DateField()
    expiration_date = models.DateField()
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ('xyz_puede_ver_cuotas', 'Puede ver cuotas'),
            ('xyz_puede_crear_cuotas', 'Puede crear cuotas'),
            ('xyz_puede_modificar_cuotas', 'Puede modificar cuotas'),
            ('xyz_puede_eliminar_cuotas', 'Puede eliminar cuotas'),
        ]


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField()
    enrollment_date = models.DateField()
    enrollment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ('xyz_puede_ver_matriculas', 'Puede ver matrículas'),
            ('xyz_puede_crear_matriculas', 'Puede crear matrículas'),
            ('xyz_puede_modificar_matriculas', 'Puede modificar matrículas'),
            ('xyz_puede_eliminar_matriculas', 'Puede eliminar matrículas'),
        ]

class PaymentMethod(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Efectivo'),
        ('credit_card', 'Tarjeta de crédito'),
        ('debit_card', 'Tarjeta de débito'),
        ('transfer', 'Transferencia'),
        ('deposit', 'Depósito'),
    )

    name = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    description = models.CharField(max_length=100, blank=True, null=True)

@receiver(post_migrate)
def create_payment_method(sender, **kwargs):
    if sender.name == 'payments':
        PaymentMethod.objects.get_or_create(name='cash', description='Efectivo')
        PaymentMethod.objects.get_or_create(name='credit_card', description='Tarjeta de crédito')
        PaymentMethod.objects.get_or_create(name='debit_card', description='Tarjeta de débito')
        PaymentMethod.objects.get_or_create(name='transfer', description='Transferencia')
        PaymentMethod.objects.get_or_create(name='deposit', description='Depósito')


class PaymentType(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('enrollment', 'Matrícula'),
        ('fee', 'Cuota'),
    )

    name = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='enrollment')
    description = models.CharField(max_length=100, blank=True, null=True)

@receiver(post_migrate)
def create_payment_type(sender, **kwargs):
    if sender.name == 'payments':
        PaymentType.objects.get_or_create(name='enrollment', description='Matrícula')
        PaymentType.objects.get_or_create(name='fee', description='Cuota')

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField()
    payment_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, null=True, blank=True)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        permissions = [
            ('xyz_puede_ver_pagos', 'Puede ver pagos'),
            ('xyz_puede_crear_pagos', 'Puede crear pagos'),
            ('xyz_puede_modificar_pagos', 'Puede modificar pagos'),
            ('xyz_puede_eliminar_pagos', 'Puede eliminar pagos'),
        ]

    
