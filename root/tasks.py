from celery import Celery
from celery.schedules import crontab
from django.conf import settings

from root.core.utils import django_setup

django_setup()

app = Celery("tasks", broker=settings.CELERY_BROKER)
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.timezone = settings.TIME_ZONE
app.conf.task_always_eager = settings.CELERY_ALWAYS_EAGER

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_CREATE_MISSING_QUEUES = True
CELERY_BROKER_TRANSPORT = "redis"
CELERY_RESULT_BACKEND = "django-db"


app.conf.beat_schedule = {
    "task_send_daily_notifications": {
        "task": "root.apps.notifications.tasks.task_send_daily_notifications",
        "schedule": crontab(hour="9", minute="0"),
        # "schedule": crontab(minute="*/1"),
    },
}

# app.autodiscover_tasks(settings.INSTALLED_APPS)
