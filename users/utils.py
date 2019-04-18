from drf_extra_fields.fields import Base64ImageField, Base64FieldMixin
from django.core.exceptions import ValidationError


VALID_IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
)


def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    if url:
        return any([url.endswith(e) for e in extension_list])
    return False


class CustomBase64Field(Base64ImageField):

    def to_internal_value(self, data):

        try:
            return Base64FieldMixin.to_internal_value(self, data)
        except (ValidationError, ValueError, ):
            return data

