from rest_framework import serializers

from news.models import *


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('avatar', 'name', 'date', 'text')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('user', 'text')


