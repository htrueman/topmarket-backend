# Generated by Django 2.1.7 on 2019-04-25 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20190425_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdelivery',
            name='place_house',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
