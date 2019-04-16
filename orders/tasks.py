import base64
import json
import subprocess
from subprocess import Popen, PIPE

import requests
from django.contrib.auth import get_user_model
from django.core.cache import cache
from odf.text import P

from top_market_platform.celery import app
from users.models import Company, MyStore

User = get_user_model()

API_BASE = 'https://api.seller.rozetka.com.ua/'


@app.task
def checkout_orders():
    for user in User.objects.all():
        if (Company.objects.filter(user=user).exists()
                and MyStore.objects.filter(user=user).exists()):
            token = cache.get('user_id_{}'.format(user.pk))
            if not token:
                if user.rozetka_username and user.rozetka_password:
                    curl_get_access_key = 'curl -X POST https://api.seller.rozetka.com.ua/sites ' \
                                   '-H \'Content-Type: application/json\' ' \
                                   '-H \'cache-control: no-cache\' ' \
                                   '-d \'{{\"username\": \"{username}\", \"password\": \"{password}\"}}\'' \
                        .format(username=user.rozetka_username,
                                password=base64.b64encode(bytes(user.rozetka_password, 'utf-8')).decode('utf-8'))

                    output = subprocess.check_output(curl_get_access_key, stderr=PIPE, shell=True)
                    data = json.loads(output)

                    # res_access_key = requests.request("POST", '{}sites'.format(API_BASE), data={
                    #     "username": user.rozetka_username,
                    #     "password": base64.b64encode(bytes(user.rozetka_password, 'utf-8')).decode('utf-8')
                    # }, headers=headers)

                    if data['success']:
                        token = data['content']['access_token']
                        cache.set('user_id_{}'.format(user.pk), token, 60 * 60 * 24)
            if token:
                curl_get_orders_key = 'curl -X GET https://api.seller.rozetka.com.ua/orders/search' \
                                      '?expand=user,delivery,order_status_history ' \
                                      '-H \'Authorization: Bearer {token}\' ' \
                                      '-H \'cache-control: no-cache\'' \
                    .format(token=token)
                output = subprocess.check_output(curl_get_orders_key, stderr=PIPE, shell=True)
                data = json.loads(output)
                print(data)
