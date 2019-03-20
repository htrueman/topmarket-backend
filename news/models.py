from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated date')

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

    avatar = models.ImageField(upload_to='new/avatars/', blank=True, null=True)
    name = models.CharField(max_length=20)
    text = models.TextField(blank=True, null=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.text

    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


class Comment(TimeStampedModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)


