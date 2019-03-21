from django.urls import path
from catalog import views as catalog_view

urlpatterns = [
    path('categories/', catalog_view.CategoryListView.as_view(), name='category_list'),
    path('categories/<str:slug>', catalog_view.CategoryRetrieveView.as_view(), name='category_retrieve'),
]
