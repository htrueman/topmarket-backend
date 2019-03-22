from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from news.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(MPTTModel):
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
        verbose_name_plural = 'categories'

    @property
    def get_category_level(self):
        return self.get_level()

    def __str__(self):
        return '{}'.format(self.slug)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)


class Product(TimeStampedModel):
    category = TreeForeignKey(
        Category,
        null=True, blank=True,
        verbose_name='Категория товара',
        on_delete=models.SET_NULL,
    )
    contractor = models.ForeignKey(
        User,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='contractors'
    )
    partners = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='Партнеры'
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

    def save(self, *args, **kwargs):
        self.slug = slugify('{}-{}'.format(self.name, self.vendor_code), allow_unicode=True)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        unique_together = (('name', 'vendor_code'), )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='catalog/products/images',
        verbose_name='Изображение товара',
    )


class ProductImageURL(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    url = models.URLField(
        verbose_name='Ссылка на изображение товара',
    )
