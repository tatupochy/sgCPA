# Generated by Django 5.0.4 on 2024-06-23 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0033_enrollment_enrollment_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fee',
            name='enrollment',
        ),
        migrations.AddField(
            model_name='fee',
            name='enrollment_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.enrollmentdetail'),
        ),
    ]
