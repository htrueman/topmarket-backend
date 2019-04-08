from django.db import models
from django.utils.translation import ugettext as _

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class KnowledgeBase(models.Model):

    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)


class TrainingModule(models.Model):
    subscriber = models.ManyToManyField(User)
    video = models.FileField(
        upload_to='marketplace/video_lessons',
        null=True, blank=True,
        verbose_name=_('Видео')
    )

    title = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name=_('Заголовок')
    )

    text = models.TextField(
        blank=True, null=True,
        verbose_name=_('Содержание')
        )

    price = models.CharField(
        max_length=20,
        blank=True, null=True,
        verbose_name=_('Цена круса')
    )


class VideoLesson(models.Model):

    training_module = models.ForeignKey('TrainingModule', on_delete=models.CASCADE)
    video = models.FileField(
        upload_to='marketplace/video_lessons',
        null=True, blank=True,
        verbose_name=_('Видео')
    )

    title = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name=_('Заголовок')
    )

    text = models.TextField(
        blank=True, null=True,
        verbose_name=_('Содержание')
    )


class ImageForLesson(models.Model):

    video_lesson = models.ForeignKey('VideoLesson', related_name='image_for_lesson', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True, verbose_name=_('Текст'))
    image = models.ImageField(
        upload_to='marketplace/images_for_lessons',
        null=True, blank=True,
        verbose_name=_('Изображение')
    )

# Инструкция добавления товара


class VideoTraining(models.Model):

    video = models.FileField(
        upload_to='marketplace/video_lessons',
        null=True, blank=True,
        verbose_name=_('Видео')
    )

    title = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name=_('Заголовок')
    )

    text = models.TextField(
        blank=True, null=True,
        verbose_name=_('Содержание')
    )


class ImageForTraining(models.Model):

    video_lesson = models.ForeignKey('VideoLesson', related_name='image_for_training', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True, verbose_name=_('Текст'))
    image = models.ImageField(
        upload_to='marketplace/images_for_lessons',
        null=True, blank=True,
        verbose_name=_('Изображение')
    )


# Дополнительные услуги

class AdditionalService(models.Model):

    buyers = models.ManyToManyField(User)
    image = models.ImageField(upload_to='marketplace/additional_service')
    title = models.TextField(blank=True, null=True, verbose_name=_('Заголовок'))
    text = models.TextField(blank=True, null=True, verbose_name=_('Текст'))
