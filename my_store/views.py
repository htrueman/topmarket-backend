from django.shortcuts import render

# Create your views here.
import requests

from rest_framework import generics
from rest_framework.response import Response
from my_store.models import MyStore, LogoWithPhones, SocialNetwork, HowToUse, Contacts, AboutUs
from users.permissions import IsOwner
from .serializers import HowToUseSerializer, ContactsSerializer, AboutUsSerializer, MyStoreDomainSerializer, \
    MyStoreInfoHeaderFooterSerializer, MyStoreSliderImagesSerializer, SocialNetworkSerializer, LogoWithPhonesSerializer
from django.db import transaction
from rest_framework import status

HOST = 'http://127.0.0.1:8080/'


class MyStoreDomainRUView(generics.RetrieveUpdateAPIView):
    queryset = MyStore.objects.all()
    serializer_class = MyStoreDomainSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = MyStore.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        transaction.set_autocommit(False)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        try:
            requests.put(
                url=HOST + 'api/shop/domain/',
                data=serializer.data
            )
            transaction.commit()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception:
            transaction.rollback()
            return Response(
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        finally:
            transaction.set_autocommit(True)


class MyStoreHeaderFooterRUView(generics.RetrieveUpdateAPIView):
    queryset = MyStore.objects.all()
    serializer_class = MyStoreInfoHeaderFooterSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = MyStore.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        transaction.set_autocommit(False)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        try:
            requests.put(
                url=HOST + 'api/shop/header_footer_info/',
                data=serializer.data
            )
            transaction.commit()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception:
            transaction.rollback()
            return Response(
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        finally:
            transaction.set_autocommit(True)


class MyStoreSliderRUView(generics.RetrieveUpdateAPIView):
    queryset = MyStore.objects.all()
    serializer_class = MyStoreSliderImagesSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = MyStore.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        transaction.set_autocommit(False)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        try:
            requests.put(
                url=HOST + 'api/shop/slider/',
                data=serializer.data
            )
            transaction.commit()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception:
            transaction.rollback()
            return Response(
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        finally:
            transaction.set_autocommit(True)


class LogoWithPhonesRUView(generics.RetrieveUpdateAPIView):
    queryset = LogoWithPhones.objects.all()
    serializer_class = LogoWithPhonesSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = LogoWithPhones.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        transaction.set_autocommit(False)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        try:
            requests.put(
                url=HOST + 'api/shop/logo_with_phones/',
                data=serializer.data
            )
            transaction.commit()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception:
            transaction.rollback()
            return Response(
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        finally:
            transaction.set_autocommit(True)


class SocialNetworkRUView(generics.RetrieveUpdateAPIView):
    queryset = SocialNetwork.objects.all()
    serializer_class = SocialNetworkSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = SocialNetwork.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        transaction.set_autocommit(False)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        try:
            requests.put(
                url=HOST + 'api/shop/networks/',
                data=serializer.data
            )
            transaction.commit()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception:
            transaction.rollback()
            return Response(
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        finally:
            transaction.set_autocommit(True)


class HowToUseRUView(generics.RetrieveUpdateAPIView):
    queryset = HowToUse
    serializer_class = HowToUseSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = HowToUse.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        transaction.set_autocommit(False)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        try:
            requests.put(
                url=HOST + 'api/shop/how_to_use/',
                data=serializer.data
            )
            transaction.commit()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception:
            transaction.rollback()
            return Response(
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        finally:
            transaction.set_autocommit(True)


class ContactsRUView(generics.RetrieveUpdateAPIView):
    queryset = Contacts
    serializer_class = ContactsSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = Contacts.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        transaction.set_autocommit(False)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        try:
            requests.put(
                url=HOST + 'api/shop/contacts/',
                data=serializer.data
            )
            transaction.commit()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception:
            transaction.rollback()
            return Response(
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        finally:
            transaction.set_autocommit(True)


class AboutUsRUView(generics.RetrieveUpdateAPIView):
    queryset = AboutUs
    serializer_class = AboutUsSerializer
    permission_classes = [IsOwner, ]

    def get_object(self):
        obj, created = AboutUs.objects.get_or_create(user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        transaction.set_autocommit(False)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        try:
            requests.put(
                        url=HOST + 'api/shop/about_us/',
                        data=serializer.data
                    )
            transaction.commit()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception:
            transaction.rollback()
            return Response(
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        finally:
            transaction.set_autocommit(True)


