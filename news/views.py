from rest_framework import viewsets, filters, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from news.mixin import LikedMixin
from .serializers import *
from .models import *


class NewsViewSet(LikedMixin, viewsets.ModelViewSet):

    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny, ]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'text')
    ordering_fields = ('name', 'text')

    def get_serializer_class(self):
        if self.action == 'like' or self.action == 'unlike' or self.action == 'fans':
            return None
        else:
            return self.serializer_class


class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = [AllowAny, ]

    def get_object(self):
        return Comment.objects.filter(news=get_object_or_404(News, pk=self.kwargs.get('news_id')))


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [AllowAny, ]

    def perform_create(self, serializer):
        serializer.save(news=get_object_or_404(News, pk=self.kwargs.get('news_id')), user=self.request.user)



