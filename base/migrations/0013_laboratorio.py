# Generated by Django 5.0.1 on 2024-06-12 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_delete_rol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_lab', models.IntegerField(unique=True)),
                ('bloque', models.IntegerField()),
                ('capacidad', models.IntegerField()),
            ],
        ),
    ]
