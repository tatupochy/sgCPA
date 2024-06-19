# Generated by Django 5.0.2 on 2024-06-15 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0024_course_matriculation_end_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='matriculation_end_date',
            new_name='enrollment_end_date',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='matriculation_start_date',
            new_name='enrollment_start_date',
        ),
        migrations.AddField(
            model_name='course',
            name='enrollment_amount',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
    ]