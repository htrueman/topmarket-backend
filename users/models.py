from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name='First name'
    )
    last_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name='Last name'
    )
    patronymic = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name='Patronymic'
    )
    email = models.EmailField(unique=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Is the user allowed to have access to the admin',
    )
    is_active = models.BooleanField(
        'active',
        default=False,
        help_text='Is the user account currently active',
    )
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
        null=True,
        blank=True
    )
    avatar = models.ImageField(blank=True, null=True, upload_to='user_profiles/avatars')

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return '{}'.format(self.get_full_name())

    def get_full_name(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.patronymic)

    def get_short_name(self):
        return '{}'.format(self.first_name)


class UserNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    new_order_email = models.BooleanField(default=False, verbose_name='Новый заказ (email)')
    new_order_tel = models.BooleanField(default=False, verbose_name='Новый заказ (смс)')
    ttn_change = models.BooleanField(default=False, verbose_name='Смена ТТН заказа')
    order_paid = models.BooleanField(default=False, verbose_name='Получение счета на оплату')
    sales_report = models.BooleanField(default=False, verbose_name='Sales report notification')
    new_message = models.BooleanField(default=False, verbose_name='New message in internal mailing notification')
    cancel_order = models.BooleanField(default=False, verbose_name='Cancel order notification')

    def __str__(self):
        return '{}'.format(self.user.get_full_name())

    class Meta:
        verbose_name = 'User notification'
        verbose_name_plural = 'User notifications'


class Company(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    name = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name='Company name'
    )

    areas_of_activity = models.TextField(
        max_length=255,
        null=True, blank=True,
        verbose_name='Сфера услуг'
    )

    logo = models.ImageField(
        upload_to='users/company/logos',
        null=True, blank=True,
        verbose_name='Лого компании',
    )

    # Тип деятельности для розничной торговли

    is_internet_shop = models.BooleanField(
        verbose_name='Интернет магазин',
        default=False
    )

    is_offline_shop = models.BooleanField(
        verbose_name='Оффлайн-магазин',
        default=False
    )


class ActivityAreas(models.Model):
    name = models.TextField(
        max_length=1095,
        verbose_name='Имя сферы деятельности'
    )

    def __str__(self):
        return '{}'.format(self.name)


class ServiceIndustry(models.Model):
    name = models.TextField(
        max_length=1095,
        verbose_name='Name service industry'
    )

    def __str__(self):
        return '{}'.format(self.name)


class CompanyType(models.Model):
    name = models.TextField(
        max_length=1095,
        verbose_name='Name company type'
    )

