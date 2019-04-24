from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.files.base import ContentFile
from django.utils.translation import ugettext as _

from .mixins import UserSerializerMixin, RequireTogetherFields
from .tokens import account_activation_token, password_reset_token
from .models import UserNotificationEmail, UserNotificationPhone, Company, ActivityAreas, ServiceIndustry, CompanyType, \
    CompanyPitch, Passport, UkraineStatistic, Certificate, TaxPayer, PayerRegister, PayerCertificate, HeaderPhoneNumber,\
    Navigation, MyStore, StoreSliderImage, FooterPhoneNumber
from .utils import CustomBase64Field, valid_url_extension
import random
import string
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .tasks import send_email_task

User = get_user_model()


class TokenObtainPairCustomSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        self.user = authenticate(**{
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        })
        print(self.user)
        is_not_activated = User.objects.filter(
            email=attrs[self.username_field],
            is_active=False
        ).exists()
        data = {}

        if is_not_activated:
            raise serializers.ValidationError(
                _('Аккаунт не активирован.')
            )

        if self.user.is_anonymous:
            raise serializers.ValidationError(
                _('Неправильный логин или пароль.'),
            )

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


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
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        mail_subject = 'Активация аккаунта.'
        message = render_to_string('account_activation_email.html', {
            'domain': settings.HOST_NAME,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        data = {
            'to_emails': [email, ],
            'subject': mail_subject,
            'html_content': message
        }
        # send_email_task.delay(**data)
        send_email_task(**data)
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
            'email': email

        })
        data = {
            'to_emails': [email, ],
            'subject': mail_subject,
            'html_content': message
        }
        # send_email_task.delay(**data)
        send_email_task(**data)
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
            data = {
                'to_emails': [email, ],
                'subject': mail_subject,
                'html_content': message
            }
            # send_email_task.delay(**data)
            send_email_task(**data)
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
    avatar_image = Base64ImageField(source='avatar', required=False)
    email_notifications = UserNotificationEmailSerializer(many=False, required=False)
    phone_notifications = UserNotificationPhoneSerializer(many=False, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'phone',
            'web_site',
            'avatar_image',
            'username',
            'email_notifications',
            'phone_notifications',
            'role',
            'user_pocket',
            'date_joined',
        )
        read_only_fields = (
            'role',
            'user_pocket',
            'date_joined',
        )

    def update(self, instance, validated_data):
        email_notifications = validated_data.pop('email_notifications', None)
        phone_notifications = validated_data.pop('phone_notifications', None)
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
        fields = ('id', 'name',)


class ServiceIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceIndustry
        fields = ('id', 'name',)


class CompanyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = ('id', 'name', )


class PassportSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(
        model_field=Passport()._meta.get_field('id'),
        required=False,
    )
    pass_doc_decoded = CustomBase64Field(
        source='pass_doc',
        required=False,
        use_url=True,
        allow_null=True
    )

    # def to_internal_value(self, data):

    class Meta:
        model = Passport
        fields = ('id', 'pass_doc_decoded',)


class UkraineStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = UkraineStatistic
        fields = ('id', 'uk_doc',)


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ('id', 'cert_doc',)


class TaxPayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxPayer
        fields = ('id', 'tax_doc',)


class PayerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayerRegister
        fields = ('id', 'payer_reg_doc',)


class PayerCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayerCertificate
        fields = ('id', 'payer_cert_doc',)


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


class CompanyRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = (
            'name',
            'town',
            'address',
            'url',
            'working_conditions',
            'logo',
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
            'activity_area',
            'service_industry',
            'company_type'
        )


class CompanyUpdateSerializer(serializers.ModelSerializer):
    logo_decoded = Base64ImageField(source='logo', required=False, allow_null=True)
    activity_area = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=ActivityAreas.objects.all()
    )

    service_industry = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=ServiceIndustry.objects.all()
    )

    company_type = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=CompanyType.objects.all()
    )

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
            'activity_area',
            'service_industry',
            'company_type'
        )


class DocumentSerializer(serializers.ModelSerializer):
    passport = PassportSerializer(many=True, source='passports', required=False)
    uk_statistic = UkraineStatisticSerializer(many=True, source='ukraine_statistics', required=False)
    certificate = CertificateSerializer(many=True, source='certificates', required=False)
    tax_payer = TaxPayerSerializer(many=True, source='tax_payers', required=False)
    payer_register = PayerRegisterSerializer(many=True, source='payer_registers', required=False)
    payer_certificate = PayerCertificateSerializer(many=True, source='payer_certificates', required=False)

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

    def update(self, instance, validated_data):
        passports_data = validated_data.pop('passports', None)
        uks_data = validated_data.pop('ukraine_statistics', None)
        certificates_data = validated_data.pop('certificates', None)
        tax_payers_data = validated_data.pop('tax_payers', None)
        registers_data = validated_data.pop('payer_registers', None)
        payer_certificates_data = validated_data.pop('payer_certificates', None)

        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if passports_data:
                for pass_data in passports_data:
                    pass_id = pass_data.get('id', None)
                    image_data = pass_data.get('pass_doc', None)
                    if pass_id:
                        is_url_field = valid_url_extension(image_data)
                        if is_url_field is not True:
                            Passport.objects.filter(id=pass_id).delete()
                    else:
                        if type(image_data) == ContentFile:
                            Passport.objects.create(company=instance, pass_doc=image_data)
            if uks_data:
                for uk_data in uks_data:
                    uk_id = uk_data.get('id', None)
                    image_data = uk_data.get('pass_doc', None)
                    if uk_id:
                        is_url_field = valid_url_extension(image_data)
                        if is_url_field is not True:
                            UkraineStatistic.objects.filter(id=uk_id).delete()
                    else:
                        if type(image_data) == ContentFile:
                            UkraineStatistic.objects.create(company=instance, uk_doc=image_data)

            if certificates_data:
                for certificate_data in certificates_data:
                    certificate_id = certificate_data.get('id', None)
                    image_data = certificate_data.get('pass_doc', None)
                    if certificate_id:
                        is_url_field = valid_url_extension(image_data)
                        if is_url_field is not True:
                            Certificate.objects.filter(id=certificate_id).delete()
                    else:
                        if type(image_data) == ContentFile:
                            Certificate.objects.create(company=instance, cert_doc=image_data)

            if tax_payers_data:
                for tax_data in tax_payers_data:
                    tax_id = tax_data.get('id', None)
                    image_data = tax_data.get('pass_doc', None)
                    if tax_id:
                        is_url_field = valid_url_extension(image_data)
                        if is_url_field is not True:
                            TaxPayer.objects.filter(id=tax_id).delete()
                    else:
                        if type(image_data) == ContentFile:
                            TaxPayer.objects.create(company=instance, tax_doc=image_data)

            if registers_data:
                for register_data in registers_data:
                    register_id = register_data.get('id', None)
                    image_data = register_data.get('pass_doc', None)
                    if register_id:
                        is_url_field = valid_url_extension(image_data)
                        if is_url_field is not True:
                            PayerRegister.objects.filter(id=register_id).delete()
                    else:
                        if type(image_data) == ContentFile:
                            PayerRegister.objects.create(company=instance, payer_reg_doc=image_data)

            if payer_certificates_data:
                for payer_certificate_data in payer_certificates_data:
                    payer_certificate_id = payer_certificate_data.get('id', None)
                    image_data = payer_certificate_data.get('pass_doc', None)
                    if payer_certificate_id:
                        is_url_field = valid_url_extension(image_data)
                        if is_url_field is not True:
                            PayerCertificate.objects.filter(id=payer_certificate_id).delete()
                    else:
                        if type(image_data) == ContentFile:
                            PayerCertificate.objects.create(company=instance, payer_cert_doc=image_data)
        return instance


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


class SliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreSliderImage
        fields = (
            'image',
        )


class MyStoreSerializer(serializers.ModelSerializer):
    header_phones_number = HeaderPhoneNumberSerializer(many=True, source='header_phones', required=False)
    footer_phones_number = FooterPhoneNumberSerializer(many=True, source='footer_phones', required=False)
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
            'header_phones_number',
            'footer_phones_number',
            'navigation',
            'slider_images',
        )

    def create(self, validated_data):
        header_phones_number_data = validated_data.pop('header_phones', None)
        footer_phones_number_data = validated_data.pop('footer_phones', None)
        navigations_data = validated_data.pop('navigation_set', None)

        my_store = MyStore.objects.create(**validated_data)

        with transaction.atomic():
            if header_phones_number_data:
                HeaderPhoneNumber.objects.bulk_create([
                    HeaderPhoneNumber(
                        store=my_store,
                        **phone
                    ) for phone in header_phones_number_data
                ])
            if footer_phones_number_data:
                FooterPhoneNumber.objects.bulk_create([
                    FooterPhoneNumber(
                        store=my_store,
                        **phone
                    ) for phone in footer_phones_number_data
                ])

            if navigations_data:
                Navigation.objects.bulk_create([
                    Navigation(
                        store=my_store,
                        **navigation_data
                    ) for navigation_data in navigations_data
                ])
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
                    HeaderPhoneNumber.objects.filter(store=instance).delete()
                    phone, _ = HeaderPhoneNumber.objects.get_or_create(
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
