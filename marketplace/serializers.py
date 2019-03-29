from django.db import transaction
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import KnowledgeBase, TrainingModule, VideoLesson, ImageForLesson, ImageForTraining, VideoTraining


class KnowledgeBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = KnowledgeBase
        fields = ('id', 'question', 'answer')


class TrainingModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainingModule
        fields = (
            'video',
            'title',
            'text',
            'price'
        )


class ImageForLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageForLesson
        fields = (
            'text',
            'image',
        )


class VideoLessonSerializer(WritableNestedModelSerializer):
    image_for_lesson = ImageForLessonSerializer(many=True, source='imageforlesson_set', required=False)

    class Meta:
        model = VideoLesson
        fields = (
            'training_module',
            'video',
            'title',
            'text',
            'image_for_lesson'
        )

    # def create(self, validated_data):
    #     image_for_lesson = validated_data.pop('imageforlesson_set', None)
    #
    #     lesson = VideoLesson.objects.create(**validated_data)
    #     with transaction.atomic():
    #         if image_for_lesson:
    #             for image_lesson in image_for_lesson:
    #                 ImageForLesson.objects.create(subscribes=lesson, **image_for_lesson)
    #     return lesson
    #
    # def update(self, instance, validated_data):
    #     image_for_lesson = validated_data.pop('imageforlesson_set', None)
    #
    #     serializers.raise_errors_on_nested_writes('update', self, validated_data)
    #     with transaction.atomic():
    #         for attr, value in validated_data.items():
    #             setattr(instance, attr, value)
    #
    #         if image_for_lesson:
    #             image_for_lesson_list = []
    #             for image_lesson in image_for_lesson:
    #                 image, _ = ImageForLesson.objects.create(
    #                     image=image_lesson['image_for_lesson'],
    #                     subscribers=instance
    #                 )
    #                 image_for_lesson_list.append(image)
    #             instance.imageforlessons = image_for_lesson_list
    #
    #         instance.save()
    #     return instance


# Инструкция по добавлению товаров
class ImageForTrainingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageForTraining
        fields = (
            'text',
            'image',
        )


class VideoTrainingSerializer(WritableNestedModelSerializer):
    image_for_lesson = ImageForLessonSerializer(many=True, source='imagefortraining_set', required=False)

    class Meta:
        model = VideoTraining
        fields = (
            'video',
            'title',
            'text',
            'image_for_lesson'
        )


