# Generated by Django 5.0.3 on 2024-04-10 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_person_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'permissions': [('xyz_puede_ver_personas', 'Puede ver personas'), ('xyz_puede_agregar_personas', 'Puede agregar personas'), ('xyz_puede_modificar_personas', 'Puede modificar personas'), ('xyz_puede_eliminar_personas', 'Puede eliminar personas')]},
        ),
    ]