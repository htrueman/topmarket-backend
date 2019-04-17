from django.contrib import admin
from .models import CustomUser, Company, MyStore, CompanyPitch

admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(MyStore)
admin.site.register(CompanyPitch)
