# Generated by Django 2.1.7 on 2019-04-15 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190415_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotificationEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_order', models.BooleanField(default=False, verbose_name='Новый заказ (email)')),
                ('ttn_change', models.BooleanField(default=False, verbose_name='Смена ТТН заказа')),
                ('order_paid', models.BooleanField(default=False, verbose_name='Получение счета на оплату')),
                ('sales_report', models.BooleanField(default=False, verbose_name='Уведомление о продажах')),
                ('new_message', models.BooleanField(default=False, verbose_name='Новое сообщение во внутреннем почтовом уведомлении')),
                ('cancel_order', models.BooleanField(default=False, verbose_name='Уведомление об отмене заказа')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='email_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Уведомление пользователя(email)',
                'verbose_name_plural': 'Увидемления пользователя(email)',
            },
        ),
        migrations.CreateModel(
            name='UserNotificationPhone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_order', models.BooleanField(default=False, verbose_name='Новый заказ (смс)')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='phone_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Уведомление пользователя(тел)',
                'verbose_name_plural': 'Увидемления пользователя(тел)',
            },
        ),
        migrations.RemoveField(
            model_name='usernotification',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserNotification',
        ),
    ]