from celery import shared_task
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from consul_kv import Connection
import logging
import os
import sys

from top_market_platform.celery import app


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
    endpoint = f'http://{consul}:8500/v1'

    conn = Connection(endpoint=endpoint)

    record = {
        f'traefik/frontends/{sub_domain}/backend': 'gen',
        f'traefik/frontends/{sub_domain}/routes/root/rule': f'Host:{sub_domain}.smartlead.top',
        'traefik/backends/gen/servers/server1/url': 'gen'
    }

    try:
        conn.put_mapping(record)
        logging.info('Reccord added {}'.format(record))
    except Exception as e:
        raise e
