from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from my_store.models import LogoWithPhones, SocialNetwork, DeliveryAndPayment, HowToUse, Contacts, HeaderPhoneNumber, \
    FooterPhoneNumber, Navigation, StoreSliderURL, AboutUs
from .models import MyStore


# Мой магазин
class HeaderPhoneNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = HeaderPhoneNumber
        fields = ('number', )


class FooterPhoneNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = FooterPhoneNumber
        fields = ('number', )


class NavigationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Navigation
        fields = ('navigation', )


class SliderUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreSliderURL
        fields = (
            'image',
        )


# Мой магазин для сгенерированого сайта
class MyStoreDomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyStore
        fields = (
            'domain_subdomain',
            'domain_name',
        )


class MyStoreInfoHeaderFooterSerializer(serializers.ModelSerializer):
    header_phones_number = HeaderPhoneNumberSerializer(many=True, source='header_phones', required=False)
    footer_phones_number = FooterPhoneNumberSerializer(many=True, source='footer_phones', required=False)
    logo_decoded = Base64ImageField(source='logo', required=False)

    class Meta:
        model = MyStore
        fields = (
            'call_back',
            'facebook',
            'instagram',
            'linkedin',
            'top_sales',
            'no_items',
            'logo_decoded',
            'header_phones_number',
            'footer_phones_number',
        )

    def update(self, instance, validated_data):
        header_phones_number_data = validated_data.pop('header_phones', None)
        footer_phones_number_data = validated_data.pop('footer_phones', None)

        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if header_phones_number_data:
                phone_list = []
                for phone_number_data in header_phones_number_data:
                    HeaderPhoneNumber.objects.filter(store=instance).delete()
                    phone, _ = HeaderPhoneNumber.objects.get_or_create(
                        store=instance,
                        **phone_number_data
                    )
                    phone_list.append(phone)
                instance.header_phones = phone_list

            if footer_phones_number_data:
                phone_list = []
                for phone_number_data in footer_phones_number_data:
                    FooterPhoneNumber.objects.filter(store=instance).delete()
                    phone, _ = FooterPhoneNumber.objects.get_or_create(
                        store=instance,
                        **phone_number_data
                    )
                    phone_list.append(phone)
                instance.footer_phones = phone_list
        instance.save()
        return instance


class MyStoreSliderImagesSerializer(serializers.ModelSerializer):
    slider_images = SliderUrlSerializer(many=True, source='storesliderimage_set', required=False, read_only=True)

    class Meta:
        model = MyStore
        fields = (
            'slider_images',
        )

    def update(self, instance, validated_data):
        store_slider = validated_data.pop('slider_urls', None)

        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            if store_slider:
                urls_list = []
                for url_data in store_slider:
                    StoreSliderURL.objects.filter(store=instance).delete()
                    url, _ = StoreSliderURL.objects.get_or_create(
                        store=instance,
                        **url_data
                    )
                    urls_list.append(url)
                instance.slider_urls = urls_list
            instance.save()
            return instance


class LogoWithPhonesSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogoWithPhones
        fields = (
            'logo',
            'shop_name',
            'first_phone',
            'second_phone',
        )


class SocialNetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialNetwork
        fields = (
            'facebook',
            'instagram',
            'twitter',
            'google',
        )


class DeliveryAndPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryAndPayment
        fields = (
            'title',
            'text',
        )


class HowToUseSerializer(serializers.ModelSerializer):

    class Meta:
        model = HowToUse
        fields = (
            'title',
            'text',
        )


class ContactsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contacts
        fields = (
            'text',
        )


class AboutUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutUs
        fields = (
            'title',
            'image',
            'text',
        )
