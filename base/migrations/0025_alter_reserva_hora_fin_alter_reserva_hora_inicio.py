# Generated by Django 5.0.1 on 2024-12-26 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_alter_laboratorio_bloque'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='hora_fin',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='hora_inicio',
            field=models.TimeField(),
        ),
    ]