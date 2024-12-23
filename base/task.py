'''from celery import shared_task
from .models import Laboratorio

@shared_task
def incrementar_capacidad_laboratorio(laboratorio_id):
    laboratorio = Laboratorio.objects.get(id=laboratorio_id)
    laboratorio.incrementar()
    laboratorio.save()'''