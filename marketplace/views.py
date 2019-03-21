from django.shortcuts import render

# Create your views here.
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny

from .models import KnowledgeBase
from .serializers import KnowledgeBaseSerializer


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

