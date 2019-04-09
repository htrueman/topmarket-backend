from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

router = DefaultRouter()
router.register(r'video-lesson', VideoLessonViewSet, base_name='video-lessons')
router.register(r'training-module', TrainingModuleViewSet, base_name='training-module')
router.register(r'video-training', VideoTrainingViewSet, base_name='video-training-for-add-items')
router.register(r'additional-service', AdditionalServiceView, base_name='additional-service')

urlpatterns = router.urls

urlpatterns += [
    path('base/', KnowledgeBaseListCreateView.as_view(), name='base-list-create'),
    path('base/<int:pk>/', KnowledgeBaseRUDView.as_view(), name='base-rud'),

]
