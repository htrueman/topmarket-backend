from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'video-lesson', views.VideoLessonViewSet, base_name='video-lessons')
router.register(r'training-module', views.TrainingModuleViewSet, base_name='training-module')
router.register(r'video-training', views.VideoTrainingViewSet, base_name='video-training-for-add-items')
router.register(r'additional-service', views.AdditionalServiceView, base_name='additional-service')

urlpatterns = router.urls

urlpatterns += [
    path('base/', views.KnowledgeBaseListCreateView.as_view(), name='base-list-create'),
    path('base/<int:pk>/', views.KnowledgeBaseRUDView.as_view(), name='base-rud'),
    path('base/contact_us/', views.ContactUsCreateView.as_view(), name='contact_us'),
    path('base/liqpay/', views.LiqPayView.as_view(), name='liqpay'),
    path('base/pocket_video/', views.GetPocketVideoView.as_view(), name='pocket_video'),
]
