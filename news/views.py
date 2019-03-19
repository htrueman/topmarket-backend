from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny

from .serializers import *
from .models import *


class NewsViewSet(viewsets.ModelViewSet):

    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]


