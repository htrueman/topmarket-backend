from django.urls import path, re_path
from drf_yasg.utils import swagger_auto_schema
from rest_framework import routers, status
from users.serializers import TokenObtainPairCustomSerializer
from users import views
from rest_framework_simplejwt import views as jwt_views
from .views import TokenObtainPairCustomView

app_name = 'users'


class ProfileRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}/$',
            mapping={'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'},
            name='{basename}-profile',
            detail=True,
            initkwargs={}
        ),
    ]


router = ProfileRouter()

router.register('profile', views.UserProfileViewSet, base_name='User')

decorated_login_view = \
   swagger_auto_schema(
      method='post',
      responses={status.HTTP_200_OK: TokenObtainPairCustomSerializer}
   )(TokenObtainPairCustomView.as_view())

urlpatterns = router.urls

urlpatterns += [
    path('register/', views.CreateUserView.as_view()),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),

    path('password_change/', views.PasswordChangeView.as_view()),

    path('login/', decorated_login_view, name='token_obtain_pair'),
    path('token_refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('company/update/', views.CompanyUpdateView.as_view(), name='retrieve_update_company'),
    path('company/detail/', views.CompanyRetrieveView.as_view(), name='retrieve_update_company'),
    path('company/activity_areas/', views.ActivityAreasListCreateView.as_view(), name='activity_areas_list_create'),
    path('company/activity_areas/<int:pk>/', views.ActivityAreasUpdateDestroyView.as_view(),
         name='activity_areas_retrieve_update_destroy'),
    path('company/service_industry/', views.ServiceIndustryListCreateView.as_view(), name='service_industry_list_create'),
    path('company/service_industry/', views.ServiceIndustryUpdateDestroyView.as_view(),
         name='service_industry_retrieve_update_destroy'),
    path('company/company_type/', views.CompanyTypeListCreateView.as_view(), name='company_type_list_create'),
    path('company/company_type/<int:pk>/', views.CompanyTypeUpdateDestroyView.as_view(),
         name='company_type_update_destroy_view'),
    path('company/documents/', views.DocumentSerializerRUView.as_view(), name='documents'),
    path('company/pitch/', views.CompanyPitchRUView.as_view(), name='pitch'),
    path('my_store/', views.MyStoreRUView.as_view(), name='my-store'),
    path('manager_create/', views.ManagerCreateView.as_view()),
    path('password_reset/', views.PasswordResetView.as_view()),
    path('send_user_miss_phone/', views.SendUserEmailAboutMissPhone.as_view(), name='miss_phone')
    # path('password_reset_confirm/', views.PasswordResetConfirmView.as_view()),
]
