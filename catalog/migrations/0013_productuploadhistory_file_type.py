# Generated by Django 2.1.7 on 2019-04-23 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_auto_20190422_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='productuploadhistory',
            name='file_type',
            field=models.CharField(choices=[('inner', 'Inner'), ('rozetka', 'Rozetka')], default='inner', max_length=7),
            preserve_default=False,
        ),
    ]