# Generated by Django 5.0.1 on 2024-10-21 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_meses'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Meses',
        ),
        migrations.AlterField(
            model_name='reserva',
            name='fecha_reserva',
            field=models.DateTimeField(),
        ),
    ]
