from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *


router = DefaultRouter()
router.register(r'news', NewsViewSet)
# router.register(r'news/comments', CommentView)


urlpatterns = router.urls

urlpatterns += [
    path('news/<int:news_id>/comments/list/', CommentListView.as_view(), name='comment_list'),
    path('news/<int:news_id>/comments/create/', CommentCreateView.as_view(), name='comment_list')
]

