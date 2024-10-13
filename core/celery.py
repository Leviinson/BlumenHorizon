import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("tasks")
app.config_from_object("blumenhorizon.core:settings", namespace="CELERY")
app.autodiscover_tasks()
