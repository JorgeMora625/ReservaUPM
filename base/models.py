from datetime import time
from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Profesores(models.Model):
    nombre = models.CharField(max_length=20, unique=False, default=None)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username 


class Alumnos(models.Model):
    nombre = models.CharField(max_length=20, unique=False, default=None)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username
    

class Laboratorio(models.Model):
    cod_lab = models.CharField(max_length=5, unique=True)
    bloque = models.CharField(max_length=3) 
    capacidad = models.IntegerField()
    capacidad_total = models.IntegerField(default=0)

    def __str__(self):
        return f'Laboratorio {self.cod_lab} del bloque {self.bloque} con capacidad para {self.capacidad_total} personas'
    
    def decrementar(self):
        if self.capacidad > 0:
            self.capacidad -= 1
            self.save()
    
    def incrementar(self):
        self.capacidad += 1
        self.save()
    
    # De moemnto no se usa
    def get_id(self):
        return self.id

    #Por consola o signal
    '''@classmethod
    def rellenar_capacidad_total(cls):
        if cls.bloque == 'CIC':
            cls.capacidad_total = 50
        elif cls.bloque == 1:
            cls.capacidad_total = 50
        elif cls.bloque == 3:
            cls.capacidad_total = 60
        elif cls.bloque == 4:
            cls.capacidad_total = 55'''

    def restablecer_capacidad(self):
        self.capacidad = self.capacidad_total
        self.save()


class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField(default=time(17, 0))
    hora_fin = models.TimeField(default=time(17, 0))
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, default=None)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""Laboratorio {self.laboratorio.cod_lab} reservado por {self.usuario.first_name} {self.usuario.last_name} para el dia {self.fecha_reserva} 
        de {self.hora_inicio} a {self.hora_fin}"""
