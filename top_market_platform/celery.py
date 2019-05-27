from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_market_platform.settings')

app = Celery('top_market_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.CELERYBEAT_SCHEDULE = {
    "set_status": {
        "task": "orders.tasks.checkout_orders",
        "schedule": crontab(minute="*/5"),
    },
    "checkout_nova_poshta_delivery_status": {
        "task": "orders.tasks.checkout_nova_poshta_delivery_status",
        "schedule": crontab(minute="*/5"),
    },
    "load_categories": {
        "task": "catalog.tasks.load_categories",
        "schedule": crontab(day_of_week="1", hour=0)
    }
}
