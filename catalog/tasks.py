from django.db import transaction
from celery import shared_task
from celery.utils.log import get_task_logger
from catalog.resources import ProductResource
from tablib import Dataset
from catalog.models import ProductUploadHistory
from django.utils.translation import ugettext as _
logger = get_task_logger(__name__)


@shared_task
def load_products_from_xls(**kwargs):
    dataset = Dataset()
    kwargs.get('instance_id')
    prod_hist = ProductUploadHistory.objects.get(id=int(kwargs.get('instance_id')))
    file_path = prod_hist.xls_file.path
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
