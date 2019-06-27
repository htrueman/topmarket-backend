import json
import time
from pprint import pprint

import requests
from django.core.cache import cache
from django.db import transaction
from celery import shared_task
from celery.utils.log import get_task_logger
from import_export.results import RowResult

from catalog.constants import ProductUploadFileTypes
from catalog.resources import ProductResource
from tablib import Dataset

from catalog.serializers import CategorySerializer
from top_market_platform.celery import app
from .models import ProductUploadHistory, Product, ProductImageURL, Category, CategoryOptionGroup, ProductOption, \
    CategoryOptionGroupValue
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError
from catalog.utils import get_rozetka_auth_token
import xlrd

logger = get_task_logger(__name__)


@shared_task
def load_products_from_xls(**kwargs):
    dataset = Dataset()
    prod_hist = ProductUploadHistory.objects.get(id=int(kwargs.get('instance_id')))
    file_path = prod_hist.xls_file.path
    if prod_hist.file_type == ProductUploadFileTypes.INNER:
        with open(file_path, 'rb') as f:
            dataset.load(f.read(), 'xls')
            product_resource = ProductResource()
            result = product_resource.import_data(
                dataset=dataset,
                dry_run=True,
                user_id=prod_hist.user.id,
            )
            print(result.invalid_rows)
            if len(dataset) > prod_hist.user.available_products_count:
                prod_hist.errors = _('У вас доступно {} свободных мест для товаров, но файл содержит {} товаров.'
                                     .format(prod_hist.user.available_products_count, len(dataset)))
                prod_hist.is_uploaded = True
                prod_hist.save()
            else:
                if not result.has_errors() and not result.has_validation_errors():
                    with transaction.atomic():
                        product_resource.import_data(
                            dataset=dataset,
                            dry_run=False,
                            user_id=prod_hist.user.id,
                            use_transactions=True,
                            collect_failed_rows=True
                        )
                        prod_hist.total_products_count = len(dataset)
                        prod_hist.user.available_products_count -= prod_hist.total_products_count
                        prod_hist.user.save()
                        prod_hist.imported_products_count = result.totals.get(RowResult.IMPORT_TYPE_NEW)
                        prod_hist.is_uploaded = True
                        prod_hist.errors = _('No errors')
                        prod_hist.save()
                else:
                    error = ''
                    for i, row in result.row_errors():
                        for err in row:
                            error += '{} {}\n'.format(i, err.error)
                    prod_hist.errors = error
                    prod_hist.save()
    elif prod_hist.file_type == ProductUploadFileTypes.ROZETKA:
        try:
            workbook = xlrd.open_workbook(file_path)
            sheet = workbook.sheet_by_index(0)
            if sheet.cell_value(rowx=0, colx=0) == 'ID товара в розетке':
                product_id_list = sheet.col_slice(0, start_rowx=1)
                list_with_zero = map(lambda x: int(x.value), product_id_list)
                result_tuple = tuple(filter(lambda x: x if x > 0 else None, list_with_zero))
            else:
                raise ValidationError(_('Invalid headers in file'))

            token_rozetka = get_rozetka_auth_token(prod_hist.user)
            # with transaction.atomic():
            if token_rozetka:
                if len(dataset) > prod_hist.user.available_products_count:
                    prod_hist.errors = _('У вас доступно {} свободных мест для товаров, но файл содержит {} товаров.'
                                         .format(prod_hist.user.available_products_count, len(dataset)))
                    prod_hist.is_uploaded = True
                    prod_hist.save()
                else:
                    count = 0
                    for product_id in result_tuple:
                        url = "https://api.seller.rozetka.com.ua/items/{product_id}" \
                              "?expand=sell_status,sold,status,description,description_ua" \
                              ",details,parent_category,status_available,group_item" \
                            .format(product_id=product_id)
                        headers = {
                            'Authorization': "Bearer {}".format(token_rozetka),
                            'cache-control': "no-cache"
                        }
                        r = requests.Request("GET", url, headers=headers)
                        prep = r.prepare()
                        s = requests.Session()
                        resp = s.send(prep)
                        r.encoding = 'utf-8'
                        data = resp.json()
                        if data['success']:
                            product = data['content']
                            try:
                                product_instance, created = Product.objects.update_or_create(
                                    rozetka_id=product.get('id'),
                                    user=prod_hist.user,
                                    defaults={
                                        'rozetka_id': product.get('id'),
                                        'user': prod_hist.user,
                                        'name': product.get('name') if product.get('name') else product.get('name_ua'),
                                        'vendor_code': int(product['article']) if product.get('article') else 0,
                                        'price': product.get('price'),
                                        'category_id': product.get('catalog_id'),
                                        'description': product.get('description')
                                        if product.get('description') else product.get('description_ua'),
                                    }
                                )
                                if created:
                                    count += 1

                                for photo in product['photo']:
                                    ProductImageURL.objects.update_or_create(
                                        product=product_instance,
                                        url=photo
                                    )
                            except Exception as e:
                                prod_hist.errors = str(e)
                        # time.sleep(0.7)
                    prod_hist.total_products_count = len(result_tuple)
                    prod_hist.user.available_products_count -= prod_hist.total_products_count
                    prod_hist.user.save()
                    prod_hist.imported_products_count = count
                    prod_hist.is_uploaded = True
                    prod_hist.save()
            else:
                prod_hist.errors = 'Неправильный логин и пароль с сервиса розетки.'
                prod_hist.is_uploaded = True
                prod_hist.save()
        except Exception:
            prod_hist.errors = 'Неправильный формат файла. После импорта с розетки, пересохраните файл!'
            prod_hist.is_uploaded = True
            prod_hist.save()


@app.task
def load_categories():
    with transaction.atomic():
        Category.load_categories()
        queryset = Category.objects.root_nodes()
        serializer = CategorySerializer(queryset, many=True)
        cache.set('categories_data', serializer.data)


@app.task
def upload_category_options():
    token = 'bnPmfhpe_nTEjUEHAbjgHh93JChyyBqQ'
    categry_ids = Category.objects.all().values_list('id', flat=True)

    # category_id = 4626923
    category_options_data = {}
    i = 1
    for category_id in categry_ids:
        try:
            url = 'https://api.seller.rozetka.com.ua/market-categories/category-options?category_id={}'.format(category_id)
            headers = {
                'Authorization': "Bearer {}".format(token),
                'cache-control': "no-cache",
            }

            r = requests.Request("GET", url, headers=headers)
            prep = r.prepare()
            s = requests.Session()
            resp = s.send(prep)
            r.encoding = 'utf-8'

            data = resp.json()
            category_options_data[category_id] = [dict(item) for item in list(data)]
            i += 1
            print(i)
        except:
            pass

        time.sleep(0.05)

    import json
    with open('result_new.json', 'w') as fp:
        json.dump(category_options_data, fp)


@app.task
def save_options_to_db():
    with open('result.json', 'rb') as fp:
        data = json.load(fp, encoding='utf-8')
        counter = 1
        print(data[str(4626923)])
        for category_id in Category.objects.all().values_list('id', flat=True):
            try:
                for option_dict in list(data[str(category_id)]):
                    print(type(dict(option_dict)))
                    # option_dict = dict(option_dict)
                    # counter += 1
                    # group, _ = CategoryOptionGroup.objects.get_or_create(
                    #     id=option_dict.get('id', None),
                    #     name=option_dict.get('name', None),
                    #     category_id=category_id
                    # )
                    # if option_dict.get('value_id', None):
                    #     option_value, _ = CategoryOptionGroupValue.objects.get_or_create(
                    #         id=option_dict.get('value_id', None),
                    #         name=option_dict.get('value_name', None)
                    #     )
            except Exception as e:
                print(e.args[0])
