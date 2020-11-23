from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from time import sleep

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FaceRecognition.settings')

app = Celery('FaceRecognition')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))



@app.task
def sum(a,b):
    return a+b


@app.task
def display(name):
    sleep(5)
    print({f'your name is {name}'})