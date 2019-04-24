from .base import *


DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_PASSWORD = "admin12admin"
EMAIL_HOST_USER = 'TopMarket'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'topmarketplatform@gmail.com'
SENDGRID_API_KEY = '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' # os.environ.get('SENDGRID_API_KEY')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}
