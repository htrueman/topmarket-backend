from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
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
    image_decoded = Base64ImageField(source='image', required=False)

    class Meta:
        model = ImageForLesson
        fields = (
            'text',
            'image_decoded',
        )


class VideoLessonSerializer(serializers.ModelSerializer):
    image_for_lesson = ImageForLessonSerializer(many=True, source='imageforlesson_set', required=False, read_only=True)

    class Meta:
        model = VideoLesson
        fields = (
            'training_module',
            'video',
            'title',
            'text',
            'image_for_lesson'
        )

    def create(self, validated_data):
        images_data = validated_data.pop('imageforlesson_set', None)
        video_lesson = VideoLesson.objects.create(**validated_data)
        if images_data:
            ImageForLesson.objects.bulk_create([
                ImageForLesson(video_lesson=video_lesson, **image_data)
                for image_data in images_data
            ])
        return video_lesson


# Инструкция по добавлению товаров
class ImageForTrainingSerializer(serializers.ModelSerializer):
    image_decoded = Base64ImageField(source='image', required=False)

    class Meta:
        model = ImageForTraining
        fields = (
            'text',
            'image_decoded',
        )


class VideoTrainingSerializer(serializers.ModelSerializer):
    image_for_lesson = ImageForLessonSerializer(many=True, source='imagefortraining_set', required=False)

    class Meta:
        model = VideoTraining
        fields = (
            'video',
            'title',
            'text',
            'image_for_lesson'
        )

    def create(self, validated_data):
        images_data = validated_data.pop('imagefortraining_set', None)
        video_training = VideoTraining.objects.create(**validated_data)
        if images_data:
            ImageForTraining.objects.bulk_create([
                ImageForTraining(video_training=video_training, **image_data)
                for image_data in images_data
            ])
        return video_training


class AdditionalServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalService
        fields = (
            'image',
            'title',
            'text',
        )
