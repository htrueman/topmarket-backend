# Generated by Django 2.1.7 on 2019-05-17 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_auto_20190517_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='available_products_count',
            field=models.PositiveIntegerField(default=200),
        ),
    ]