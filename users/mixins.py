from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions


class RequireTogetherFields:
    REQUIRED_TOGETHER = tuple()

    def validate(self, data):
        for field in self.REQUIRED_TOGETHER:
            if field not in self.fields.keys():
                raise serializers.ValidationError('Field {} is not specified.'.format(field))

        data_values = [data.get(key) for key in self.REQUIRED_TOGETHER]
        if not all(data_values) and any(data_values):
            raise serializers.ValidationError('Fields ' + ', '.join(self.REQUIRED_TOGETHER) + ' are required together.')
        return super().validate(data)


class UserSerializerMixin:
    def validate(self, data):
        password = data.get('password')
        if password:
            errors = dict()
            try:
                validators.validate_password(password=password)
            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)
            if errors:
                raise serializers.ValidationError(errors)
            if data.get('password') != data.get('confirm_password'):
                errors['password'] = "The two password fields didn't match."
                raise serializers.ValidationError(errors)
        return super().validate(data)
