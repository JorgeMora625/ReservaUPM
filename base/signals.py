from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from  .models import Profesores, Alumnos, Laboratorio
        
@receiver(post_save, sender=User)
def crea_rol_ususrio(sender, instance, created, **kwargs):
    if created:
        if '@alumnos.upm.es' in instance.email:
            Alumnos.objects.create(nombre=instance.first_name, usuario=instance)
        elif '@upm.es' in instance.email:
            Profesores.objects.create(nombre=instance.first_name, usuario=instance)


@receiver(post_save, sender=Laboratorio)
def asignar_capacidad_total(sender, instance, created, **kwargs):
    if created:
        if instance.bloque == 'CIC' or instance.bloque == '1':
            instance.capacidad_total = 50
        elif instance.bloque == '3':
            instance.capacidad_total = 60
        elif instance.bloque == '4':
            instance.capacidad_total = 55
        
        instance.save()

