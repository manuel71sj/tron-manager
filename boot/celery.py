import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boot.settings")

app = Celery("TRONManager")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

"""
celery multi start w1 -A boot.celery --loglevel=info -E
celery --broker=amqp://tronmanager:dYvca5-sibcur-pydpec@129.154.59.231:5672/TronManager flower
"""

app.conf.worker_cancel_long_running_tasks_on_connection_loss = True
app.conf.update(
    CELERYBEAT_SCHEDULE={
        "check_wallet_status": {
            "task": "transaction.tasks.check_wallet_status",
            "schedule": timedelta(minutes=10),
            "args": (),
        },
    }
)
