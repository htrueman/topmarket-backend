from django.shortcuts import render

# Create your views here.
from rest_framework import generics, filters, viewsets
from rest_framework.permissions import AllowAny

from .models import KnowledgeBase, VideoLesson, TrainingModule
from .serializers import KnowledgeBaseSerializer, VideoLessonSerializer, TrainingModuleSerializer


class KnowledgeBaseListCreateView(generics.ListCreateAPIView):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [AllowAny, ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('question', 'answer')


class KnowledgeBaseRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [AllowAny, ]


class TrainingModuleViewSet(viewsets.ModelViewSet):
    queryset = TrainingModule.objects.all()
    serializer_class = TrainingModuleSerializer


class VideoLessonViewSet(viewsets.ModelViewSet):
    queryset = VideoLesson.objects.all()
    serializer_class = VideoLessonSerializer
