# Generated by Django 5.0.2 on 2024-06-07 22:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0002_alter_attendance_options'),
        ('students', '0015_course_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='present',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='student',
        ),
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present', models.BooleanField()),
                ('attendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendances.attendance')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='students',
            field=models.ManyToManyField(through='attendances.AttendanceRecord', to='students.student'),
        ),
    ]