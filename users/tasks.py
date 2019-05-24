from celery import shared_task
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from consul_kv import Connection
import logging
import os
import sys

from top_market_platform.celery import app
from users.models import CustomUser

User = get_user_model()

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
        print(e.args)


@app.task
def generate_store(sub_domain):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    consul = os.getenv('CONSUL', 'localhost')
    front_srv = os.getenv('FRONT_SRV', 'http://gen')
    endpoint = f'http://{consul}:8500/v1'
    sub_domain = sub_domain.lower()
    conn = Connection(endpoint=endpoint)

    record = {
        f'traefik/frontends/{sub_domain}/backend': 'gen',
        f'traefik/frontends/{sub_domain}/routes/root/rule': f'Host:{sub_domain}.smartlead.top',
        'traefik/backends/gen/servers/server1/url': f'{front_srv}'
    }

    try:
        conn.put_mapping(record)
        logging.info('Reccord added {}'.format(record))
    except Exception as e:
        raise e


def send_user_email():

    users = CustomUser.objects.all().filter(id__gte=10)
    message = render_to_string('send_email_enter_phone.html')

    data = {
        'to_emails': list(users.values_list('email', flat=True)),
        'subject': "Регистрация на платформе “Smartlead 2.0”",
        'html_content': message,
    }

    send_email_task(**data)
