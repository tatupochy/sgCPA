# Generated by Django 5.0.2 on 2024-03-09 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userroles'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
