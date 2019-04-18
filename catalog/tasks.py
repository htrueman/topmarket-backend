from django.db import transaction
from celery import shared_task
from celery.utils.log import get_task_logger
from catalog.resources import ProductResource
from tablib import Dataset
from catalog.models import ProductUploadHistory
import itertools

logger = get_task_logger(__name__)


@shared_task
def load_products_from_xls(**kwargs):
    product_resource = ProductResource()
    dataset = Dataset()
    kwargs.get('instance_id')
    prod_hist = ProductUploadHistory.objects.get(id=int(kwargs.get('instance_id')))
    file_path = prod_hist.xls_file.path
    with open(file_path, 'rb') as f:
        dataset.load(f.read(), 'xls')
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
                prod_hist.errors = 'No errors'
                prod_hist.save()
        else:
            prod_hist.errors = '. '.join(itertools.chain.from_iterable([x.error.messages for x in result.invalid_rows]))
            prod_hist.save()
