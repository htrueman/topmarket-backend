from django.contrib import admin
from .models import CustomUser, Company

admin.site.register(CustomUser)
admin.site.register(Company)
