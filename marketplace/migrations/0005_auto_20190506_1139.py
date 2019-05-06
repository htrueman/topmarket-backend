# Generated by Django 2.1.7 on 2019-05-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0004_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='phone',
            field=models.CharField(default='+38', max_length=32, verbose_name='Телефон'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contactus',
            name='email',
            field=models.EmailField(default='mail@mail.com', max_length=254, verbose_name='Електронная почта'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contactus',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст сообщения'),
        ),
    ]