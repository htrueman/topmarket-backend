# Generated by Django 2.1.7 on 2019-04-17 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20190417_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='system_comment',
            field=models.TextField(blank=True),
        ),
    ]
