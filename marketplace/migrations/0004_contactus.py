# Generated by Django 2.1.7 on 2019-04-24 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0003_auto_20190415_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Имя')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Електронная почта')),
                ('subject', models.CharField(blank=True, max_length=256, null=True, verbose_name='Тема сообщения')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Свяжитесь с нами',
                'verbose_name_plural': 'Свяжитесь с нами',
            },
        ),
    ]
