from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey
from news.models import TimeStampedModel
from django.contrib.auth import get_user_model
import catalog.constants as constants
from django.db import transaction
from .utils import get_category_data
from catalog.managers import ContractorProductManager, PartnerProductManager
User = get_user_model()


class Category(MPTTModel):
    id = models.PositiveIntegerField(
        primary_key=True,
        verbose_name='id - primary key',
    )
    name = models.CharField(
        max_length=256,
        verbose_name=_('Название категории'),
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.SET_NULL,
        db_index=True,
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    @property
    def get_category_level(self):
        return self.get_level()

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)

    @staticmethod
    def load_categories():
        """

        python manage.py load_categories

        :return: None
        """
        data = get_category_data()
        with transaction.atomic():
            with Category.objects.disable_mptt_updates():
                for obj in data['content']['marketCategorys']:
                    if int(obj['parent_id']) > 0:
                        parent, created_parent = Category.objects.get_or_create(
                            id=int(obj['parent_id'])
                        )
                        if created_parent:
                            parent.name = 'instance'
                            parent.save()
                    else:
                        parent = None
                    instance, _ = Category.objects.get_or_create(
                        id=int(obj['category_id']),
                    )
                    instance.name = obj['name']
                    instance.parent = parent
                    instance.save()
            Category.objects.rebuild()


class Product(TimeStampedModel):
    """
    Если поле contractor=NULL - товар добавлен поставщиком.
    В противном случае это товар, добавленный партнером от поставщика
    """

    category = TreeForeignKey(
        Category,
        null=True, blank=True,
        verbose_name=_('Категория товара'),
        on_delete=models.SET_NULL,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='products',
    )

    contractor_product = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Связь с поставщиком продукта'),
        related_name='contractor_products',
    )

    availability = models.CharField(
        max_length=13,
        verbose_name=_('Доступность товара'),
        choices=constants.PRODUCT_AVAILABILITY,
        default='IN_STOCK'
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Имя продукта')
    )
    vendor_code = models.CharField(
        max_length=63,
        verbose_name=_('Артикул'),
    )
    product_type = models.CharField(
        max_length=256,
        verbose_name=_('Вид товара')
    )
    brand = models.CharField(
        max_length=255,
        verbose_name=_('Бренд'),
    )
    count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Наличие'),
    )
    description = models.TextField(
        max_length=4095,
        null=True, blank=True,
        verbose_name=_('Описание'),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, blank=True,
        verbose_name=_('Цена товара'),
    )

    # managers
    objects = models.Manager()
    products_by_contractors = ContractorProductManager()
    products_by_parnters = PartnerProductManager()

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
        unique_together = (('user', 'contractor_product', 'vendor_code',),)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        super(Product, self).save(force_insert, force_update, using, update_fields)


class ProductImageURL(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    url = models.URLField(
        verbose_name=_('Ссылка на изображение товара'),
    )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='catalog/products/images',
        verbose_name=_('Изображение товара'),
    )


class YMLTemplate(models.Model):
    template = models.FileField(
        upload_to='yml_templates',
    )
    yml_type = models.CharField(
        max_length=10,
        choices=constants.YMLFileTypes.YML_TYPES,
        primary_key=True
    )

    def __str__(self):
        return self.yml_type

    class Meta:
        verbose_name = _('YML шаблон')
        verbose_name_plural = _('YML шаблоны')
