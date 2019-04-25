import base64
import json
import subprocess

from django.core.cache import cache


def get_category_data():
    with open('catalog/categories.json') as f:
        data = json.load(f)
        return data


def get_rozetka_auth_token(user):
    token_rozetka = cache.get('user_id_{}'.format(user.pk))
    if not token_rozetka:
        if user.rozetka_username and user.rozetka_password:
            curl_get_access_key = 'curl -X POST https://api.seller.rozetka.com.ua/sites ' \
                                  '-H \'Content-Type: application/json\' ' \
                                  '-H \'cache-control: no-cache\' ' \
                                  '-d \'{{\"username\": \"{username}\", \"password\": \"{password}\"}}\'' \
                .format(username=user.rozetka_username,
                        password=base64.b64encode(bytes(user.rozetka_password, 'utf-8')).decode('utf-8'))

            output = subprocess.check_output(curl_get_access_key, stderr=subprocess.PIPE, shell=True)
            data = json.loads(output)

            if data['success']:
                token_rozetka = data['content']['access_token']
                cache.set('user_id_{}'.format(user.pk), token_rozetka, 60 * 60 * 24)
    return token_rozetka


data = [
    {
        'id': 1,
        'parent': None,
        'name': 'qwerty1'
    },
    {
        'id': 2,
        'parent': 1,
        'name': 'qwerty2'
    },
    {
        'id': 3,
        'parent': 1,
        'name': 'qwerty3'
    },
    {
        'id': 4,
        'parent': 3,
        'name': 'qwerty4'
    },
    {
        'id': 5,
        'parent': None,
        'name': 'qwerty5'
    },
    {
        'id': 6,
        'parent': 5,
        'name': 'qwerty6'
    }
]


# class Node(dict):
#     def __init__(self, id, name):
#         self.name = name
#         self.id = id
#         self.subcategories = []
#
#     def child(self):



# def get_tree(data=None):
#     _internal_data = {}
#     for item in data:
#         all_data = []
#         if item['parent'] is None:
#             root_id = item['id']
#             _internal_data = {}
#             _internal_data['id'] = item['id']
#             _internal_data['name'] = item['name']
#             _internal_data['subcategories'] = []
#             continue
#         if _internal_data['id'] == item['parent']:

query = [{'id': 1, 'desc': 'desc_father', 'parent_id': None}
    , {'id': 2, 'desc': 'desc_child_1', 'parent_id': 1}
    , {'id': 3, 'desc': 'desc_child_2', 'parent_id': 2}
    , {'id': 4, 'desc': 'desc_child_5', 'parent_id': 5}
    , {'id': 5, 'desc': 'desc_child_6', 'parent_id': 6}
    , {'id': 6, 'desc': 'desc_child_1', 'parent_id': 1}]


def rec(query, parent):
    parent['children'] = []
    for item in query:
        if item['parent_id'] == parent['id']:
            parent['children'].append(item)
            rec(query, item)
