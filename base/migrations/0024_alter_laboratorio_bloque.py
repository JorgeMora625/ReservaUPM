# Generated by Django 5.0.1 on 2024-12-22 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_alter_laboratorio_cod_lab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratorio',
            name='bloque',
            field=models.CharField(max_length=3),
        ),
    ]