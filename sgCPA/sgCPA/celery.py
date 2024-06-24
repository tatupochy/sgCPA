# sgCPA/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el módulo de configuración predeterminado para 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgCPA.settings')

app = Celery('sgCPA')

# Lee la configuración desde el archivo settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre y carga tareas definidas en cada paquete de aplicaciones Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


