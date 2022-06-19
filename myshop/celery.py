import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop', backend=settings.REDIS_HOST, backend=settings.REDIS_HOST)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
