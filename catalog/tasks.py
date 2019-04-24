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

from catalog.utils import get_rozetka_auth_token

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
        token_rozetka = get_rozetka_auth_token(prod_hist.user)

        if not token_rozetka:
            curl_get_orders_key = 'curl -X GET https://api.seller.rozetka.com.ua/items/58898602' \
                                  '?expand=user,delivery,order_status_history ' \
                                  '-H \'Authorization: Bearer {token_rozetka}\' ' \
                                  '-H \'cache-control: no-cache\'' \
                .format(token_rozetka=prod_hist.user)
            output = subprocess.check_output(curl_get_orders_key, stderr=subprocess.PIPE, shell=True)
            data = json.loads(output)
