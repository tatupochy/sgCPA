# Generated by Django 5.0.2 on 2024-06-08 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0006_remove_attendance_students_delete_attendancerecord'),
        ('students', '0022_coursedates_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='students',
            field=models.ManyToManyField(through='attendances.AttendanceRecord', to='students.student'),
        ),
    ]