# Generated by Django 2.1.7 on 2019-04-04 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20190403_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcontractor',
            name='availability',
            field=models.CharField(choices=[('NOT_AVAILABLE', 'Нет в наличии'), ('EXPECTED_DELIVERY', 'Ожидается поставка'), ('CAUSED', 'Вызывается'), ('IS_ENDING', 'Заканчивается'), ('IN_STOCK', 'В наличии'), ('IN_ARCHIVE', 'В архиве'), ('NOT_IN_STOCK', 'Нет на складе'), ('HIDDEN', 'Скрытый')], default='IN_STOCK', max_length=13, verbose_name='Доступность товара'),
        ),
        migrations.AddField(
            model_name='productcontractor',
            name='product_code',
            field=models.CharField(default=1, max_length=63, verbose_name='Код товара'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productpartner',
            name='availability',
            field=models.CharField(choices=[('NOT_AVAILABLE', 'Нет в наличии'), ('EXPECTED_DELIVERY', 'Ожидается поставка'), ('CAUSED', 'Вызывается'), ('IS_ENDING', 'Заканчивается'), ('IN_STOCK', 'В наличии'), ('IN_ARCHIVE', 'В архиве'), ('NOT_IN_STOCK', 'Нет на складе'), ('HIDDEN', 'Скрытый')], default='IN_STOCK', max_length=13, verbose_name='Доступность товара'),
        ),
        migrations.AddField(
            model_name='productpartner',
            name='product_code',
            field=models.CharField(default=1, max_length=63, verbose_name='Код товара'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='productcontractor',
            unique_together={('vendor_code', 'product_code')},
        ),
    ]
