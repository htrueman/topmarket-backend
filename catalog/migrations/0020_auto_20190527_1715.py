# Generated by Django 2.1.7 on 2019-05-27 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_remove_product_validated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimageurl',
            name='url',
            field=models.URLField(max_length=1000, verbose_name='Ссылка на изображение товара'),
        ),
    ]
