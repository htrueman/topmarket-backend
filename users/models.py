from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

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

    def save(self, *args, **kwargs):
        if self.is_staff:
            self.role = 'admin'
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.email)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


