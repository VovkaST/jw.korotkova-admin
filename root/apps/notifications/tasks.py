import asyncio

from celery import shared_task

from root.apps.notifications.services import NotificationsDailyService


@shared_task
def task_send_daily_notifications():
    service = NotificationsDailyService()
    return asyncio.run(service.send_daily_notifications())
