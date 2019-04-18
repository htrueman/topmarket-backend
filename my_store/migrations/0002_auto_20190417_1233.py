# Generated by Django 2.1.7 on 2019-04-17 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreSliderURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(blank=True, null=True, verbose_name='Картинка для слайдера')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slider_urls', to='my_store.MyStore')),
            ],
        ),
        migrations.RemoveField(
            model_name='storesliderimage',
            name='store',
        ),
        migrations.AddField(
            model_name='contacts',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='StoreSliderImage',
        ),
    ]
