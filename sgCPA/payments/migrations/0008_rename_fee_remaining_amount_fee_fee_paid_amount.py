# Generated by Django 5.0.4 on 2024-05-25 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_fee_fee_remaining_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fee',
            old_name='fee_remaining_amount',
            new_name='fee_paid_amount',
        ),
    ]