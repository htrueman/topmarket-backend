from django.db import models
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
        null=True, blank=True
    )

    title = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name='Заголовок'
    )

    text = models.TextField(
        blank=True, null=True,
        verbose_name='Содержание'
        )

    price = models.CharField(
        max_length=20,
        blank=True, null=True,
        verbose_name='Цена круса'
    )


class VideoLesson(models.Model):

    training_module = models.ForeignKey('TrainingModule', on_delete=models.CASCADE)
    video = models.FileField(
        upload_to='marketplace/video_lessons',
        null=True, blank=True
    )

    title = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name='Заголовок'
    )

    text = models.TextField(
        blank=True, null=True,
        verbose_name='Содержание'
    )


class ImageForLesson(models.Model):

    video_lesson = models.ForeignKey('VideoLesson', related_name='image_for_lesson', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='marketplace/images_for_lessons',
        null=True, blank=True
    )

# Инструкция добавления товара


class VideoTraining(models.Model):

    video = models.FileField(
        upload_to='marketplace/video_lessons',
        null=True, blank=True
    )

    title = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name='Заголовок'
    )

    text = models.TextField(
        blank=True, null=True,
        verbose_name='Содержание'
    )


class ImageForTraining(models.Model):

    video_lesson = models.ForeignKey('VideoLesson', related_name='image_for_training', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='marketplace/images_for_lessons',
        null=True, blank=True
    )


