# Generated by Django 5.0.2 on 2024-06-13 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0022_coursedates_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='maxStudentsNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='minStudentsNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]