# Generated by Django 5.0.2 on 2024-06-16 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0025_rename_matriculation_end_date_course_enrollment_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='space_available',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]