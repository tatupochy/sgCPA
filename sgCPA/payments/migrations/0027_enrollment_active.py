# Generated by Django 4.2.10 on 2024-06-16 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0026_remove_enrollment_students_enrollment_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='active',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
