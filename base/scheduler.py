from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from .models import Laboratorio

def incrementar_capacidad(cod_lab):
    lab = Laboratorio.objects.get(cod_lab=cod_lab)
    lab.incrementar() #lab.capacidad += 1
    lab.save()

def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    
    fecha_ejecucion = datetime.now() + timedelta(days=1)
    fecha_ejecucion = fecha_ejecucion.replace(hour=10, minute=0)

    #lab = request.session
    
    # Programar la tarea
    scheduler.add_job(incrementar_capacidad, 'date', run_date=fecha_ejecucion)
    scheduler.start()

# Para que se inicie el scheduler al importar este módulo
iniciar_scheduler()