# Generated by Django 5.0.2 on 2024-06-08 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0017_alter_course_days_per_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='days_per_week',
        ),
    ]
