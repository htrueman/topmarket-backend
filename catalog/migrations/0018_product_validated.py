# Generated by Django 2.1.7 on 2019-05-21 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_auto_20190517_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='validated',
            field=models.BooleanField(default=False, verbose_name='Is validated'),
        ),
    ]