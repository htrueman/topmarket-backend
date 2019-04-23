from celery import shared_task
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings


@shared_task
def send_email_task(*args, **kwargs):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = Mail(
        from_email=from_email,
        **kwargs
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        pass
