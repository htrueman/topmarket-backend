# Generated by Django 2.1.7 on 2019-04-25 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20190425_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderuser',
            name='rozetka_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
