from celery import Celery
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selteq_task.settings')

app = Celery('selteq_task')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()
