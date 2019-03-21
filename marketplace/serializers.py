from rest_framework import serializers

from .models import KnowledgeBase


class KnowledgeBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = KnowledgeBase
        fields = ('id', 'question', 'answer')

