# Generated by Django 5.0.1 on 2024-11-02 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_laboratorio_capacidad_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='hora_fin',
            field=models.TimeField(default=datetime.time(17, 0)),
        ),
        migrations.AddField(
            model_name='reserva',
            name='hora_inicio',
            field=models.TimeField(default=datetime.time(17, 0)),
        ),
    ]
