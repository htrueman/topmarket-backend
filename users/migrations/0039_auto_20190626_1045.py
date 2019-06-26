# Generated by Django 2.1.7 on 2019-06-26 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0038_customuser_product_percent'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='customuser',
        #     name='product_percent',
        # ),
        migrations.AddField(
            model_name='customuser',
            name='percent_for_partner',
            field=models.SmallIntegerField(default=5, verbose_name='Процент для продавца'),
        ),
    ]
