from django.db.models.signals import post_save
from django.dispatch import receiver

from catalog.constants import ProductUploadFileTypes
from catalog.models import ProductUploadHistory
from catalog.tasks import load_products_from_xls


@receiver(post_save, sender=ProductUploadHistory)
def upload_product_from_xls(sender, instance, created, **kwargs):
    if created:
        data = {
            'instance_id': instance.id,
        }
        load_products_from_xls.delay(**data)
        # load_products_from_xls(**data)
        # if instance.file_type == ProductUploadFileTypes.INNER:
        #     # load_products_from_xls.delay(**data)
        #     load_products_from_xls(**data)
