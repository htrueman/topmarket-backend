from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
import pdfkit
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment

from django.conf import settings

from .models import KnowledgeBase, TrainingModule, VideoLesson, ImageForLesson, ImageForTraining, VideoTraining, \
    AdditionalService, ContactUs
from users.tasks import send_email_task


User = get_user_model()


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


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = (
            'name',
            'email',
            'phone',
            'subject',
            'text',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_anonymous:
            instance = ContactUs.objects.create(**validated_data)
        else:
            instance = ContactUs.objects.create(
                **validated_data,
                user=user,
                email=user.email,
                name=user.get_full_name()
            )
        return instance


class LiqPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_pocket',
        )

    def update(self, instance, validated_data):
        user = self.context['request'].user
        mail_subject = 'Покупка пакета'
        message = render_to_string('liqpay.html', {
            'pocket': validated_data['user_pocket'],
        })

        data = {
            'to_emails': [user.email, ],
            'subject': mail_subject,
            'html_content': message
        }

        pdfkit.from_string('TEST', 'smart_lead_pocket_paid.pdf')
        from_email = settings.DEFAULT_FROM_EMAIL
        message = Mail(
            from_email=from_email,
            **data,
        )
        attachment = Attachment()
        with open('smart_lead_pocket_paid.pdf', 'rb') as f:
            attachment.file_content = base64.b64encode(f.read()).decode('utf-8')
        attachment.file_name = 'smart_lead_pocket_paid.pdf'
        message.add_attachment(attachment)

        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)

        # send_email_task.delay(**data)
        return super().update(instance, validated_data)
