# Generated by Django 4.2.10 on 2024-06-22 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0018_attendancesettings'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AttendanceSettings',
        ),
    ]
