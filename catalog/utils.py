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
            url = "https://api.seller.rozetka.com.ua/sites"
            headers = {
                'Content-Type': 'application/json',
            }
            payload = {
                'username': user.rozetka_username,
                'password': base64.b64encode(bytes(user.rozetka_password, 'utf-8')).decode('utf-8'),
            }
            r = requests.Request("POST", url, json=payload, headers=headers)
            prep = r.prepare()
            s = requests.Session()
            resp = s.send(prep)
            r.encoding = 'utf-8'
            data = resp.json()

            if data['success']:
                token_rozetka = data['content']['access_token']
                cache.set('user_id_{}'.format(user.pk), token_rozetka, 60 * 60 * 24)
    return token_rozetka


def _filter(_d):
  return {a:b for a, b in _d.items() if a != 'parent'}


def group_vals(_d, _start=None):
  return list(
      _filter({**i, 'subcategories': group_vals(_d, i['id'])})
      for i in _d if i['parent'] == _start
  )


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
