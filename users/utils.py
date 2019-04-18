from drf_extra_fields.fields import Base64ImageField, Base64FieldMixin
from django.core.exceptions import ValidationError
from rest_framework.fields import URLField, ImageField


VALID_IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
)


def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    return any([url.endswith(e) for e in extension_list])


class CustomBase64Field(Base64ImageField):

    def to_internal_value(self, data):
        print(ImageField)
        print(type(data))
        print(type(data) == str)
        print(data)
        try:
            return Base64FieldMixin.to_internal_value(self, data)
        except ValidationError:
            return

