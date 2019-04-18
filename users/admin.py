from django.contrib import admin
from .models import CustomUser, Company, MyStore, CompanyPitch, Passport

admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(MyStore)
admin.site.register(CompanyPitch)
admin.site.register(Passport)
