from django.contrib import admin
from .models import CustomUser, Company,  CompanyPitch
from my_store.models import MyStore
admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(MyStore)
admin.site.register(CompanyPitch)
