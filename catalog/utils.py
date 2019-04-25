import base64
import json
import subprocess

import requests
from django.core.cache import cache


def get_category_data():
    with open('catalog/categories.json') as f:
        data = json.load(f)
        return data


def get_rozetka_auth_token(user):
    token_rozetka = cache.get('user_id_{}'.format(user.pk))
    if not token_rozetka:
        if user.rozetka_username and user.rozetka_password:
            # curl_get_access_key = 'curl -X POST https://api.seller.rozetka.com.ua/sites ' \
            #                       '-H \'Content-Type: application/json\' ' \
            #                       '-H \'cache-control: no-cache\' ' \
            #                       '-d \'{{\"username\": \"{username}\", \"password\": \"{password}\"}}\'' \
            #     .format(username=user.rozetka_username,
            #             password=base64.b64encode(bytes(user.rozetka_password, 'utf-8')).decode('utf-8'))
            #
            # output = subprocess.check_output(curl_get_access_key, stderr=subprocess.PIPE, shell=True)
            # data = json.loads(output)

            url = "https://api.seller.rozetka.com.ua/sites"
            querystring = {
                "expand": "sell_status,sold,status,description,"
                          "description_ua,details,parent_category,status_available,group_item"}
            headers = {
                'Content-Type': 'application/json',
            }
            payload = {
                'username': user.rozetka_username,
                'password': base64.b64encode(bytes(user.rozetka_password, 'utf-8')).decode('utf-8'),
            }
            r = requests.Request("POST", url, data=payload, headers=headers, params=querystring)
            prep = r.prepare()
            s = requests.Session()
            resp = s.send(prep)
            r.encoding = 'utf-8'
            data = resp.json()

            if data['success']:
                token_rozetka = data['content']['access_token']
                cache.set('user_id_{}'.format(user.pk), token_rozetka, 60 * 60 * 24)
    return token_rozetka
