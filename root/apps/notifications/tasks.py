import asyncio

from celery import shared_task

from root.apps.notifications.application.interactors.notifications_daily import NotificationsDailyInteractor


@shared_task
def task_send_daily_notifications():
    notifications_interactor = NotificationsDailyInteractor()
    return asyncio.run(notifications_interactor.send_daily_notifications())
