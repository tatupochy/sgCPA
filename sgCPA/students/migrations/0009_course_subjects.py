# Generated by Django 5.0.2 on 2024-03-29 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_alter_student_course'),
        ('subjects', '0002_subject_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='subjects',
            field=models.ManyToManyField(to='subjects.subject'),
        ),
    ]