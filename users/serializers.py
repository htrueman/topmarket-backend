from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .mixins import UserSerializerMixin, RequireTogetherFields
from .tokens import account_activation_token, password_reset_token

User = get_user_model()


class UserSerializer(UserSerializerMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'confirm_password')

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
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, (email,))
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self):
        email = self.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            mail_subject = 'Reset your project_W password.'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': password_reset_token.make_token(user),
            })
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, (email,))
        else:
            errors = dict()
            errors['email'] = "The user with given email does not exist."
            raise serializers.ValidationError(errors)


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


class UserProfileSerializer(RequireTogetherFields, UserSerializerMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    avatar_image = serializers.ImageField(source='avatar', required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'confirm_password', 'avatar_image', 'username', )

    REQUIRED_TOGETHER = ('password', 'confirm_password',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

