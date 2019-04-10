from celery import shared_task
from celery.utils.log import get_task_logger
from catalog.resources import ProductResource
from tablib import Dataset
from pprint import pprint
logger = get_task_logger(__name__)


@shared_task
def load_products_from_xls(**kwargs):
    product_resource = ProductResource()
    dataset = Dataset()
    file = kwargs.get('file')
    print(file.read())
    # imported_data = dataset.load(file.read())
    # pprint(imported_data)
    pass


