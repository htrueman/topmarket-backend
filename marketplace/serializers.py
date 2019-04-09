from django.db import transaction
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import KnowledgeBase, TrainingModule, VideoLesson, ImageForLesson, ImageForTraining, VideoTraining, \
    AdditionalService


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


class AdditionalServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalService
        fields = (
            'image',
            'title',
            'text',
        )
