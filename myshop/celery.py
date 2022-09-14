import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop', broker='redis://137803e4-8dbd-4742-bd1a-a30600ec7c16@us1-singular-goldfish-38274.upstash.io')
# app = Celery('myshop', broker='amqps://bccqdxkt:id-B_tDR0ilKms9CSPR0PRTqvjIhge2K@woodpecker.rmq.cloudamqp.com/bccqdxkt')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
