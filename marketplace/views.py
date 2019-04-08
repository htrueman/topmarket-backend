from rest_framework.response import Response
from rest_framework import generics, filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import KnowledgeBase, VideoLesson, TrainingModule, VideoTraining, AdditionalService
from .serializers import KnowledgeBaseSerializer, VideoLessonSerializer, TrainingModuleSerializer, \
    VideoTrainingSerializer, AdditionalServiceSerializer


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

    @action(detail=True, methods=['POST'], serializer_class=None)
    def add_to_my_products(self, request, pk, **kwargs):
        product = get_object_or_404(TrainingModule, pk=pk)
        product.subscriber.add(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], serializer_class=None)
    def remove_from_my_products(self, request, pk, **kwargs):
        product = get_object_or_404(TrainingModule, pk=pk)
        product.subscriber.remove(request.user)
        return Response(status=status.HTTP_200_OK)


class VideoLessonViewSet(viewsets.ModelViewSet):
    queryset = VideoLesson.objects.all()
    serializer_class = VideoLessonSerializer


class VideoTrainingViewSet(viewsets.ModelViewSet):
    queryset = VideoTraining.objects.all()
    serializer_class = VideoTrainingSerializer


class AdditionalServiceView(viewsets.ModelViewSet):
    queryset = AdditionalService.objects.all()
    serializer_class = AdditionalServiceSerializer

    @action(detail=True, methods=['POST'], serializer_class=None)
    def add_buyer(self, request, pk, **kwargs):
        service = get_object_or_404(AdditionalService, pk=pk)
        service.buyers.add(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], serializer_class=None)
    def check_additional_service_permission(self, request, pk, **kwargs):
        service = get_object_or_404(AdditionalService, pk=pk)
        try:
            user = service.buyers.get(pk=request.user.id)
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
