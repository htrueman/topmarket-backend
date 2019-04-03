# Generated by Django 2.1.7 on 2019-04-01 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0002_auto_20190327_1445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.RemoveField(
            model_name='productpartner',
            name='partners',
        ),
        migrations.AddField(
            model_name='productpartner',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='партнер'),
        ),
        migrations.AddField(
            model_name='productpartner',
            name='product_by_contractor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.ProductContractor', verbose_name='продукция поставщика'),
        ),
    ]