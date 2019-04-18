from django.shortcuts import render

# Create your views here.
import requests
from rest_framework import generics

from my_store.models import MyStore, LogoWithPhones, SocialNetwork, HowToUse, Contacts, AboutUs
from users.permissions import IsOwner
from .serializers import HowToUseSerializer, ContactsSerializer, AboutUsSerializer, MyStoreDomainSerializer, \
    MyStoreInfoHeaderFooterSerializer, MyStoreSliderImagesSerializer, SocialNetworkSerializer

HOST = 'http://127.0.0.1:8080/'


class MyStoreDomainRUView(generics.RetrieveUpdateAPIView):
    queryset = MyStore.objects.all()
    serializer_class = MyStoreDomainSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = MyStore.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        result = super().update(request, *args, **kwargs)
        serializer = self.serializer_class()
        requests.post(
            url=HOST + 'v1/domain/',
            data=serializer.data
        )
        return result


class MyStoreHeaderFooterRUView(generics.RetrieveUpdateAPIView):
    queryset = MyStore.objects.all()
    serializer_class = MyStoreInfoHeaderFooterSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = MyStore.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        result = super().update(request, *args, **kwargs)
        serializer = self.serializer_class()
        print(serializer.data)
        return result


class MyStoreSliderRUView(generics.RetrieveUpdateAPIView):
    queryset = MyStore.objects.all()
    serializer_class = MyStoreSliderImagesSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = MyStore.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        result = super().update(request, *args, **kwargs)
        serializer = self.serializer_class()
        print(serializer.data)
        return result


class LogoWithPhonesRUView(generics.RetrieveUpdateAPIView):
    queryset = LogoWithPhones.objects.all()
    serializer_class = LogoWithPhones
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = LogoWithPhones.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        result = super().update(request, *args, **kwargs)
        serializer = self.serializer_class()
        print(serializer.data)
        return result


class SocialNetworkRUView(generics.RetrieveUpdateAPIView):
    queryset = SocialNetwork.objects.all()
    serializer_class = SocialNetworkSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = SocialNetwork.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        result = super().update(request, *args, **kwargs)
        serializer = self.serializer_class(data=request.data)
        print(serializer.data)
        requests.put(
            url=HOST + 'api/shop/networks/',
            data=serializer.data
        )
        return result


class HowToUseRUView(generics.RetrieveUpdateAPIView):
    queryset = HowToUse
    serializer_class = HowToUseSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = HowToUse.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        result = super().update(request, *args, **kwargs)
        serializer = self.serializer_class()
        print(serializer.data)
        return result


class ContactsRUView(generics.RetrieveUpdateAPIView):
    queryset = Contacts
    serializer_class = ContactsSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = Contacts.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        result = super().update(request, *args, **kwargs)
        serializer = self.serializer_class()
        print(serializer.data)
        return result


class AboutUsRUView(generics.RetrieveUpdateAPIView):
    queryset = AboutUs
    serializer_class = AboutUsSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = AboutUs.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        result = super().update(request, *args, **kwargs)
        serializer = self.serializer_class()
        requests.post
        return result
