# Generated by Django 2.1.7 on 2019-05-06 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_auto_20190506_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Електронная почта'),
        ),
    ]