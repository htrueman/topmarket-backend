from django.db import models


class ContractorProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(contractor_product__isnull=True)


class PartnerProductManager(models.Manager):
    def get_queryset(self):
        return super(PartnerProductManager, self).get_queryset().filter(contractor_product__isnull=False)
