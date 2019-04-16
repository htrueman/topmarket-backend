from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .mixins import UserSerializerMixin, RequireTogetherFields
from .tokens import account_activation_token, password_reset_token
from .models import UserNotificationEmail, UserNotificationPhone, Company, ActivityAreas, ServiceIndustry, CompanyType, \
    CompanyPitch, Passport, UkraineStatistic, Certificate, TaxPayer, PayerRegister, PayerCertificate, PhoneNumber,\
    Navigation, MyStore, StoreSliderImage

import random
import string

User = get_user_model()


class UserSerializer(UserSerializerMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'confirm_password', 'role')

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.create(
            email=email,
        )
        user.set_password(validated_data['password'])
        user.save()
        mail_subject = 'Activate your account.'
        message = render_to_string('account_activation_email.html', {
            'domain': settings.HOST_NAME,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email,])

        return user


class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', )

    def create(self, validated_data):
        email = validated_data['email']
        request = self.context.get('request')

        company = get_object_or_404(Company, user=request.user)
        user = User.objects.create(
            email=email,
            manager=company,
        )
        first_name = validated_data['first_name']
        user.first_name = first_name
        password = self.generate_password(10)
        user.set_password(password)
        user.save()
        mail_subject = 'Invitation to TOP MARKET PLACE'
        message = render_to_string('manager_invitation.html', {
            'domain': settings.HOST_NAME,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
            'password': password,
        })
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email,])
        return user

    @staticmethod
    def generate_password(string_length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(string_length))


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self, *args):
        email = self.validated_data['email']
        user = User.objects.filter(email=email).first()
        password = self.generate_password(10)
        user.set_password(password)
        user.save()
        if user:
            mail_subject = 'Reset your topmarket password.'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'password': password
            })
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, (email,))
            return password
        else:
            errors = dict()
            errors['email'] = "The user with given email does not exist."
            raise serializers.ValidationError(errors)

    class Meta:
        fields = (
            'email',
        )

    @staticmethod
    def generate_password(string_length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(string_length))


class PasswordResetConfirm(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        password = data.get('new_password')
        errors = dict()
        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors['new_password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        if data.get('new_password') != data.get('confirm_password'):
            errors['new_password'] = "Those passwords don't match."
            raise serializers.ValidationError(errors)
        return super(PasswordResetConfirm, self).validate(data)

    def save(self):
        uid = self.validated_data['uid']
        token = self.validated_data['token']
        errors = dict()
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            errors['uid'] = "Invalid uid."
            raise serializers.ValidationError(errors)
        if user and password_reset_token.check_token(user, token):
            user.set_password(self.validated_data['new_password'])
            user.save()
        else:
            errors['token'] = "Invalid token."
            raise serializers.ValidationError(errors)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        password = data.get('new_password')
        errors = dict()
        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors['new_password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        if data.get('new_password') != data.get('confirm_password'):
            errors['new_password'] = "Those passwords don't match."
            raise serializers.ValidationError(errors)
        return super(PasswordChangeSerializer, self).validate(data)


class UserNotificationEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationEmail
        fields = (
            'new_order',
            'ttn_change',
            'order_paid',
            'sales_report',
            'new_message',
            'cancel_order',
        )


class UserNotificationPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationPhone
        fields = (
            'new_order',
        )


class UserProfileSerializer(RequireTogetherFields, UserSerializerMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    avatar_image = Base64ImageField(source='avatar', required=False)
    email_notifications = UserNotificationEmailSerializer(many=False, required=False)
    phone_notifications = UserNotificationPhoneSerializer(many=False, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'patronymic',
            'phone',
            'web_site',
            'avatar_image',
            'username',
            'email_notifications',
            'phone_notifications',
        )

    REQUIRED_TOGETHER = ('password', 'confirm_password',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        email_notifications = validated_data.pop('email_notifications', None)
        phone_notifications = validated_data.pop('phone_notifications', None)
        if password:
            instance.set_password(password)
        if email_notifications:
            notification, _ = UserNotificationEmail.objects.get_or_create(
                user=self.context['request'].user,
            )
            for attr, value in email_notifications.items():
                setattr(notification, attr, value)
            notification.save()

        if phone_notifications:
            notification, _ = UserNotificationPhone.objects.get_or_create(
                user=self.context['request'].user,
            )
            for attr, value in phone_notifications.items():
                setattr(notification, attr, value)
            notification.save()
        return super().update(instance, validated_data)


class ActivityAreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityAreas
        fields = ('name',)


class ServiceIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceIndustry
        fields = ('name',)


class CompanyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = ('name', )


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = ('pass_doc',)


class UkraineStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = UkraineStatistic
        fields = ('uk_doc',)


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ('cert_doc',)


class TaxPayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxPayer
        fields = ('tax_doc',)


class PayerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayerRegister
        fields = ('payer_reg_doc',)


class PayerCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayerCertificate
        fields = ('payer_cert_doc',)


class CompanyPitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPitch
        fields = (
            'who_are_you',
            'guru',
            'for_whom',
            'difference',
            'good_partner',
            'future'
        )


class CompanySerializer(serializers.ModelSerializer):
    logo_decoded = Base64ImageField(source='logo', required=False, allow_null=True)

    class Meta:
        model = Company
        fields = (
            'name',
            'town',
            'address',
            'url',
            'working_conditions',
            'logo_decoded',
            'web_site',
            'phone',
            'email',
            'who_see_contact',
            'is_internet_shop',
            'is_offline_shop',
            'retail_network',
            'distributor',
            'manufacturer',
            'importer',
            'dealer',
            'sub_dealer',
            'exporter',
            'official_representative',
            'about_company',
        )


class DocumentSerializer(serializers.ModelSerializer):
    passport = PassportSerializer(many=True, source='passport_set', required=False)
    uk_statistic = UkraineStatisticSerializer(many=True, source='ukrainestatistic_set', required=False)
    certificate = CertificateSerializer(many=True, source='certificate_set', required=False)
    tax_payer = TaxPayerSerializer(many=True, source='taxpayer_set', required=False)
    payer_register = PayerRegisterSerializer(many=True, source='payerregister_set', required=False)
    payer_certificate = PayerCertificateSerializer(many=True, source='payercertificate_set', required=False)

    class Meta:
        model = Company
        fields = (
            'passport',
            'uk_statistic',
            'certificate',
            'tax_payer',
            'payer_register',
            'payer_certificate',
        )

    def create(self, validated_data):

            passport_data = validated_data.pop('passport_set', None)
            uk_data = validated_data.pop('ukrainestatistic_set', None)
            certificate_data = validated_data.pop('certificate_set', None)
            tax_payer_data = validated_data.pop('taxpayer_set', None)
            register_data = validated_data.pop('payerregister_set', None)
            payer_certificate = validated_data.pop('payercertificate_set', None)

            company = Company.objects.create(**validated_data)

            with transaction.atomic():
                if passport_data:
                    for passport in passport_data:
                        Passport.objects.create(company=company, **passport)
                if uk_data:
                    for uk_stat in uk_data:
                        UkraineStatistic.objects.create(company=company, **uk_stat)
                if certificate_data:
                    for certificate in certificate_data:
                        Certificate.objects.create(company=company, **certificate)
                if tax_payer_data:
                    for tax in tax_payer_data:
                        TaxPayer.objects.create(company=company, **tax)
                if register_data:
                    for register in register_data:
                        PayerRegister.objects.create(company=company, **register)
                if payer_certificate:
                    for payer_cert in payer_certificate:
                        PayerCertificate.objects.create(company=company, **payer_cert)
            return company

    def update(self, instance, validated_data):
            passports_data = validated_data.pop('passport_set', None)
            uks_data = validated_data.pop('ukrainestatistic_set', None)
            certificates_data = validated_data.pop('certificates_set', None)
            tax_payers_data = validated_data.pop('taxpayer_set', None)
            registers_data = validated_data.pop('payerregister_set', None)
            payer_certificates_data = validated_data.pop('payercertificate_set', None)

            serializers.raise_errors_on_nested_writes('update', self, validated_data)
            with transaction.atomic():
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)

                if passports_data:
                    passport_list = []
                    for passport_data in passports_data:
                        passport, _ = Passport.objects.get_or_create(
                            pass_doc=passport_data['passports'],
                            company=instance
                        )
                        passport_list.append(passport)
                    instance.passports = passport_list

                if uks_data:
                    uk_list = []
                    for uk_data in uks_data:
                        uk, _ = UkraineStatistic.objects.get_or_create(
                            uk_doc=uk_data['ukraine_statistics'],
                            company=instance
                        )
                        uk_list.append(uk)
                    instance.ukraine_statistics = uk_list

                if certificates_data:
                    cert_list = []
                    for certificate_data in certificates_data:
                        certificate, _ = Certificate.objects.get_or_create(
                            cert_doc=certificate_data['certificates'],
                            company=instance
                        )
                        cert_list.append(certificate)
                    instance.certificates = cert_list

                if tax_payers_data:
                    tax_payer_list = []
                    for tax_payer_data in tax_payers_data:
                        tax_payer, _ = TaxPayer.objects.get_or_create(
                            tax_doc=tax_payer_data['tax_payers'],
                            company=instance
                        )
                        tax_payer_list.append(tax_payer)
                    instance.tax_payers = tax_payer_list
                if registers_data:
                    register_list = []
                    for register_data in registers_data:
                        register, _ = PayerRegister.objects.get_or_create(
                            payer_reg_doc=register_data['payer_registers'],
                            company=instance
                        )
                        register_list.append(register)
                    instance.payer_registers = register_list
                if payer_certificates_data:
                    payer_cert_list = []
                    for payer_certificate_data in payer_certificates_data:
                        payer_certificate, _ = PayerCertificate.objects.get_or_create(
                            payer_cert_doc=payer_certificate_data['payer_certificates'],
                            company=instance
                        )
                        payer_cert_list.append(payer_certificate)
                    instance.payer_certificates = payer_cert_list

                instance.save();
            return instance


# Мой магазин
class PhoneNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhoneNumber
        fields = ('number', )


class NavigationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Navigation
        fields = ('navigation', )


class SliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreSliderImage
        fields = (
            'image',
        )


class MyStoreSerializer(serializers.ModelSerializer):
    phones_number = PhoneNumberSerializer(many=True, source='phonenumber_set', required=False)
    navigation = NavigationSerializer(many=True, source='navigation_set', required=False)
    slider_images = SliderImageSerializer(many=True, source='storesliderimage_set', required=False)
    logo_decoded = Base64ImageField(source='logo', required=False)

    class Meta:
        model = MyStore
        fields = (
            'domain_subdomain',
            'domain_name',
            'call_back',
            'facebook',
            'instagram',
            'linkedin',
            'top_sales',
            'no_items',
            'logo_decoded',
            'phones_number',
            'navigation',
            'slider_images',
        )

    def create(self, validated_data):
        phones_number_data = validated_data.pop('phone_set', None)
        navigations_data = validated_data.pop('navigation_set', None)

        my_store = MyStore.objects.create(**validated_data)

        with transaction.atomic():
            if phones_number_data:
                for phone_number_data in phones_number_data:
                    PhoneNumber.objects.create(store=my_store, **phone_number_data)

            if navigations_data:
                for navigation_data in navigations_data:
                    Navigation.objects.create(store=my_store, **navigation_data)

        return my_store

    def update(self, instance, validated_data):
        phones_number_data = validated_data.pop('phonenumber_set', None)
        navigations_data = validated_data.pop('navigation_set', None)

        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if phones_number_data:
                phone_list = []
                for phone_number_data in phones_number_data:
                    print(phone_number_data)
                    phone, _ = PhoneNumber.objects.get_or_create(
                        number=phone_number_data['phones'],
                        store=instance
                    )
                    phone_list.append(phone)
                instance.numbers = phone_list

            if navigations_data:
                navigation_list = []
                for navigation_data in navigations_data:
                    navigation, _ = Navigation.objects.get_or_create(
                        navigation=navigation_data['navigations'],
                        store=instance
                    )
                    navigation_list.append(navigation)
                instance.navigations = navigation_list

            instance.save()
        return instance







