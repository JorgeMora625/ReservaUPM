'''from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Configura el archivo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

app = Celery('proyecto')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() #lambda:settings.INSTALLED_APPS'''