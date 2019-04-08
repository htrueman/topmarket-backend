from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from news.models import TimeStampedModel
from django.contrib.auth import get_user_model
import catalog.constants as constants
from django.db import transaction
from .utils import get_category_data

User = get_user_model()


class Category(MPTTModel):
    id = models.PositiveIntegerField(
        primary_key=True,
        verbose_name='id - primary key',
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        db_index=True,
        max_length=512,
        allow_unicode=True,
        verbose_name='Slug',
        unique=True
    )
    parent = TreeForeignKey(
        'self',
        null=True, blank=True,
        related_name='children',
        on_delete=models.SET_NULL,
        db_index=True
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ('parent', 'slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    @property
    def get_category_level(self):
        return self.get_level()

    def __str__(self):
        return '{}'.format(self.slug)

    def save(self, *args, **kwargs):
        self.slug = slugify('{}-{}'.format(self.name, self.id), allow_unicode=True)
        super(Category, self).save(*args, **kwargs)

    @staticmethod
    def load_categories():
        """

        python manage.py shell
        from catalog.models import Category
        Category.load_categories()

        :return: none
        """
        data = get_category_data()
        with transaction.atomic():
            with Category.objects.disable_mptt_updates():
                for obj in data:
                    if int(obj['parent_id'] > 0):
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
                    instance.name = str(obj['name']),
                    instance.parent = parent
                    instance.save()
            Category.objects.rebuild()


class ProductAbstract(TimeStampedModel):
    category = TreeForeignKey(
        Category,
        null=True, blank=True,
        verbose_name='Категория товара',
        on_delete=models.SET_NULL,
    )
    availability = models.CharField(
        max_length=13,
        verbose_name='Доступность товара',
        choices=constants.PRODUCT_AVAILABILITY,
        default='IN_STOCK'
    )
    slug = models.SlugField(
        max_length=511,
        db_index=True,
        allow_unicode=True,
        verbose_name='Slug',
        unique=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Имя продукта'
    )
    vendor_code = models.CharField(
        max_length=63,
        verbose_name='Артикул',
    )
    product_code = models.CharField(
        max_length=63,
        verbose_name='Код товара'
    )
    brand = models.CharField(
        max_length=255,
        verbose_name='Бренд',
        null=True, blank=True,
    )
    count = models.PositiveIntegerField(
        default=0,
        verbose_name='Наличие',
    )
    description = models.TextField(
        max_length=4095,
        null=True, blank=True,
        verbose_name='Описание',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, blank=True,
        verbose_name='Цена товара',
    )

    def __str__(self):
        return '{0}'.format(self.slug)

    class Meta:
        abstract = True


class ProductContractor(ProductAbstract):
    contractor = models.ForeignKey(
        User,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='Поставщик',
        related_name='contractors',
        db_index=True
    )

    class Meta:
        verbose_name = 'Товар (как поставщик)'
        verbose_name_plural = 'Товары (как поставщик)'
        unique_together = (('vendor_code', 'product_code'),)


class ProductContractorImage(models.Model):
    product = models.ForeignKey(
        ProductContractor,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='catalog/products/contractor/images',
        verbose_name='Изображение товара',
    )


class ProductContractorImageURL(models.Model):
    product = models.ForeignKey(
        ProductContractor,
        on_delete=models.CASCADE
    )
    url = models.URLField(
        verbose_name='Ссылка на изображение товара',
    )


class ProductPartner(ProductAbstract):
    partner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='партнер',
    )
    product_by_contractor = models.ForeignKey(
        ProductContractor,
        on_delete=models.CASCADE,
        verbose_name='продукция поставщика',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Мой товар (добавленный от поставшика)'
        verbose_name_plural = 'Мои товары (добавленные от поставщика)'
        unique_together = (('partner', 'product_by_contractor'),)


class ProductPartnerImage(models.Model):
    product = models.ForeignKey(
        ProductPartner,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='catalog/products/images',
        verbose_name='Изображение товара',
    )


class ProductPartnerImageURL(models.Model):
    product = models.ForeignKey(
        ProductPartner,
        on_delete=models.CASCADE
    )
    url = models.URLField(
        verbose_name='Ссылка на изображение товара',
    )
