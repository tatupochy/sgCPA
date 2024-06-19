# Generated by Django 5.0.3 on 2024-06-14 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0022_alter_concept_related_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='enrollment',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='fee',
        ),
        migrations.AddField(
            model_name='stamping',
            name='valid_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paymenttype',
            name='name',
            field=models.CharField(choices=[('enrollment', 'Matrícula'), ('fee', 'Cuota'), ('invoice', 'Factura')], default='enrollment', max_length=20),
        ),
    ]