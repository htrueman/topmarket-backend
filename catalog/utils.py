import json


def get_category_data():
    with open('catalog/categories.json') as f:
        data = json.load(f)
        return data
