from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        abstract = True


class Like(models.Model):
    user = models.ForeignKey(User,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class News(TimeStampedModel):

    avatar = models.ImageField(upload_to='news/avatars/', blank=True, null=True, verbose_name=_('Аватар'))
    name = models.CharField(max_length=20)
    text = models.TextField(blank=True, null=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.text

    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = _('Новость')
        verbose_name_plural = _('Новости')


class Comment(TimeStampedModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE, blank=True, null=True , verbose_name=_('Новости'))
    text = models.TextField(blank=True, null=True, verbose_name=_('Комментарий'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')
