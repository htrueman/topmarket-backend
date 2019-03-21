from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

urlpatterns = [
    path('base/', KnowledgeBaseListCreateView.as_view(), name='base-list-create'),
    path('base/<int:pk>/', KnowledgeBaseRUDView.as_view(), name='base-rud'),
]
