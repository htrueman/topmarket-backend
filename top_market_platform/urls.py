from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAdminUser, AllowAny
from django.conf import settings
from django.conf.urls.static import static


class CategorizedAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys):
        if len(operation_keys) >= 1:
            operation_keys = operation_keys[1:]
        return super().get_tags(operation_keys)


schema_view = get_schema_view(
    openapi.Info(
      title="Top Market Platform API",
      default_version='v1',
    ),
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui(), name='docs'),
    path('api/<version>/', include('users.urls')),
    path('api/<version>/news/', include('news.urls')),
    path('api/<version>/marketplace/', include('marketplace.urls')),
    path('api/<version>/catalog/', include('catalog.urls')),
    path('api/<version>/my_store/', include('my_store.urls'))
] \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


