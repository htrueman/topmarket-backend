from django.db import models
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

    @property
    def is_have_children(self):
        if self.get_descendant_count() > 0:
            return True
        return False

    def __str__(self):
        return '{}'.format(self.name)

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
        null=True,
        blank=True,
        verbose_name=_('Категория товара'),
        on_delete=models.SET_NULL,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='products',
    )

    # product full name fields
    product_type = models.CharField(
        max_length=256,
        verbose_name=_('Вид товара')
    )
    brand = models.CharField(
        max_length=255,
        verbose_name=_('Бренд')
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Имя продукта')
    )
    variety_type = models.CharField(
        max_length=256,
        verbose_name=_('Название разновидности'),
        null=True,
        blank=True
    )
    vendor_code = models.CharField(
        max_length=63,
        verbose_name=_('Артикул'),
    )

    # required product specs
    warranty_duration = models.PositiveIntegerField(default=0)  # warranty duration in days
    vendor_country = models.CharField(
        max_length=256
    )
    box_size = models.CharField(
        max_length=256
    )
    count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Наличие'),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Цена товара'),
    )
    description = models.TextField(
        max_length=4095,
        verbose_name=_('Описание'),
    )  # html tags allowed

    # not required product specs
    extra_description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Дополнительные характеристики')
    )  # html tags allowed
    age_group = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_('Возрастная группа')
    )
    material = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_('Материал товара')
    )

    contractor_product = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Связь с поставщиком продукта'),
        related_name='contractor_products',
    )

    rozetka_id = models.IntegerField(
        null=True,
        blank=True
    )

    # managers
    objects = models.Manager()
    products_by_contractors = ContractorProductManager()
    products_by_partners = PartnerProductManager()

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        if self.count == 0:
            return False
        return True

    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
        unique_together = (
            ('user', 'product_type', 'brand', 'name', 'variety_type', 'vendor_code', 'contractor_product'),
        )


class ProductImageURL(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_image_urls'
    )
    url = models.URLField(
        verbose_name=_('Ссылка на изображение товара'),
    )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_images'
    )
    image = models.ImageField(
        upload_to='catalog/products/images',
        verbose_name=_('Изображение товара'),
    )


class ProductUploadHistory(models.Model):
    user = models.ForeignKey(
        User,
        related_name='product_import_files',
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    is_uploaded = models.BooleanField(
        verbose_name=_('Загрузка прошла успешно'),
        default=False,
    )
    errors = models.TextField(
        verbose_name=_('Ошибки'),
        null=True, blank=True,
    )
    xls_file = models.FileField(
        upload_to='catalog/product/uploads',
        verbose_name=_('XLS файл')
    )
    file_type = models.CharField(
        max_length=7,
        choices=constants.ProductUploadFileTypes.PRODUCT_UPLOAD_FILE_TYPES
    )
    total_products_count = models.PositiveIntegerField(default=0)
    imported_products_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = _('Файл для импорта товаров')
        verbose_name_plural = _('Файлы для импорта товаров')


class YMLTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    template = models.FileField(
        upload_to='yml_templates',
    )
    yml_type = models.CharField(
        max_length=10,
        choices=constants.YMLFileTypes.YML_TYPES
    )
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.yml_type

    class Meta:
        verbose_name = _('YML шаблон')
        verbose_name_plural = _('YML шаблоны')
        unique_together = ('user', 'yml_type',)
