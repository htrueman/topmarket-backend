from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

app_name = 'news'

router = DefaultRouter()
router.register(r'', NewsViewSet, base_name='News')
# router.register(r'news/comments', CommentView)


urlpatterns = router.urls

urlpatterns += [
    path('<int:news_id>/comments/list/', CommentListView.as_view(), name='comment_list'),
    path('<int:news_id>/comments/create/', CommentCreateView.as_view(), name='comment_list')
]

