import os
import sys

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.dev")

app: Celery = Celery('project')
app.config_from_object('project.settings.celery', namespace="celery")

if 'test' in sys.argv[1:]:
    app.config_from_object('project.settings.test', namespace="celery")

app.autodiscover_tasks(['cronjobs'])
