import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boot.settings')

app = Celery('TRONManager')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

'''
celery multi start w1 -A boot.celery --loglevel=info -E
celery --broker=amqp://tronmanager:dYvca5-sibcur-pydpec@129.154.59.231:5672/TronManager flower
'''
