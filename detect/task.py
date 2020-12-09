from __future__ import absolute_import, unicode_literals
from celery import shared_task
from . import notify


@shared_task
def detect(name,location):
    notify.send_notify(name,location)
