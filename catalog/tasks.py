import json
import subprocess
from contextlib import suppress

import requests
from django.db import transaction, IntegrityError
from celery import shared_task
from celery.utils.log import get_task_logger

from catalog.constants import ProductUploadFileTypes
from catalog.resources import ProductResource
from tablib import Dataset
from .models import ProductUploadHistory, Product, ProductImageURL
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError
from catalog.utils import get_rozetka_auth_token
import xlrd
import time

logger = get_task_logger(__name__)


@shared_task
def load_products_from_xls(**kwargs):
    dataset = Dataset()
    kwargs.get('instance_id')
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

            if not result.has_errors() and not result.has_validation_errors():
                with transaction.atomic():
                    product_resource.import_data(
                        dataset=dataset,
                        dry_run=False,
                        user_id=prod_hist.user.id,
                        use_transactions=True,
                        collect_failed_rows=True
                    )
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
        workbook = xlrd.open_workbook(file_path)
        sheet = workbook.sheet_by_index(0)
        if sheet.cell_value(rowx=0, colx=0) == 'ID товара в розетке':
            product_id_list = sheet.col_slice(0, start_rowx=1)
            list_with_zero = map(lambda x: int(x.value), product_id_list)
            result_tuple = tuple(filter(lambda x: x if x > 0 else None, list_with_zero))
        else:
            raise ValidationError(_('Invalid headers in file'))

        token_rozetka = get_rozetka_auth_token(prod_hist.user)
        with transaction.atomic():
            if token_rozetka:
                for product_id in result_tuple:
                    # curl_get_orders_key = 'curl -X GET https://api.seller.rozetka.com.ua/items/{product_id}' \
                    #                       '?expand=sell_status,sold,status,description,description_ua,' \
                    #                       'details,parent_category,status_available,group_item ' \
                    #                       '-H \'Authorization: Bearer {token_rozetka}\' ' \
                    #                       '-H \'cache-control: no-cache\'' \
                    #     .format(token_rozetka=token_rozetka, product_id=product_id)
                    # output = subprocess.check_output(curl_get_orders_key, stderr=subprocess.PIPE, shell=True)
                    # data = json.loads(output)

                    url = "https://api.seller.rozetka.com.ua/items/{product_id}" \
                          "?expand=sell_status,sold,status,description,description_ua" \
                          ",details,parent_category,status_available,group_item"\
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
                        # Массажер для чистки лица + POBLING + Sonic Pore Cleansing Brush + Golden
                        full_name = product.get('name') if product.get('name') else product.get('name_ua')

                        with suppress(IntegrityError):
                            product_instance, created = Product.objects.update_or_create(
                                rozetka_id=product['id'],
                                user=prod_hist.user,
                                defaults={
                                    'name': product.get('name') if product.get('name') else product.get('name_ua'),
                                    'vendor_code': product['article'],
                                    'price': product['price'],
                                    'category_id': product['catalog_id'],
                                    'description': product.get('description')
                                    if product.get('description') else product.get('description_ua'),
                                }
                            )

                            for photo in product['photo']:
                                ProductImageURL.objects.update_or_create(
                                    product=product_instance,
                                    url=photo
                                )
                    time.sleep(0.7)

                prod_hist.is_uploaded = True
                prod_hist.save()
        return token_rozetka
