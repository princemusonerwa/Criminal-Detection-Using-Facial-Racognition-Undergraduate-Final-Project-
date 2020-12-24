from __future__ import absolute_import, unicode_literals
from celery import shared_task
from . import notify
from .detection import train

@shared_task
def detect(name,location):
    notify.send_notify(name,location)

@shared_task
def trainData():
    train()
    print("trained data successfully")
