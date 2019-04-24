import json
import subprocess

from django.db import transaction
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.cache import cache

from catalog.constants import ProductUploadFileTypes
from catalog.resources import ProductResource
from tablib import Dataset
from catalog.models import ProductUploadHistory
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError
from catalog.utils import get_rozetka_auth_token
import xlrd


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
        result_tuple = ()
        if sheet.cell_value(rowx=0, colx=0) == 'ID товара в розетке':
            product_id_list = sheet.col_slice(0, start_rowx=1)
            list_with_zero = map(lambda x: int(x.value), product_id_list)
            result_tuple = tuple(filter(lambda x: x if x > 0 else None, list_with_zero))
        else:
            raise ValidationError(_('Invalid headers in file'))

        token_rozetka = get_rozetka_auth_token(prod_hist.user)
        if token_rozetka:
            curl_get_orders_key = 'curl -X GET https://api.seller.rozetka.com.ua/items/58898602' \
                                  '?expand=sell_status,sold,status,description,description_ua,' \
                                  'details,parent_category,status_available,group_item ' \
                                  '-H \'Authorization: Bearer {token_rozetka}\' ' \
                                  '-H \'cache-control: no-cache\'' \
                .format(token_rozetka=token_rozetka)
            output = subprocess.check_output(curl_get_orders_key, stderr=subprocess.PIPE, shell=True)
            data = json.loads(output)
            if data['success']:
                pass
