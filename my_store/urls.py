from django.urls import path, re_path

from .views import LogoWithPhonesRUView, SocialNetworkRUView, HowToUseRUView, ContactsRUView, \
    AboutUsRUView, MyStoreDomainRUView, MyStoreHeaderFooterRUView, MyStoreSliderRUView

app_name = 'my_store'

urlpatterns = [
    path('my_store/domain', MyStoreDomainRUView.as_view(), name='domain'),
    path('my_store/header_footer', MyStoreHeaderFooterRUView.as_view(), name='header_footer'),
    path('my_store/domain', MyStoreSliderRUView.as_view(), name='slider'),
    path('my_store/login_with_phones/', LogoWithPhonesRUView.as_view(), name='login_with_phones'),
    path('my_store/social_network/', SocialNetworkRUView.as_view(), name='social_network'),
    path('my_store/how_to_use/', HowToUseRUView.as_view(), name='how_ti_use'),
    path('my_store/contacts/', ContactsRUView.as_view(), name='contacts'),
    path('my_store/about_us/', AboutUsRUView.as_view(), name='about_us'),


]