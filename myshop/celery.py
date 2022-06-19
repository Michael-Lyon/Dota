import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop', broker='redis-12153.c257.us-east-1-3.ec2.cloud.redislabs.com:12153')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
