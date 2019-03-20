from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

urlpatterns = [

    path('base/list-create/', KnowledgeBaseListCreateView.as_view(), name='base-list-create'),
    path('base/rud/', KnowledgeBaseRUDView.as_view(), name='base-rud')
]