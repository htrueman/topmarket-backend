from django.contrib import admin
from .models import CustomUser, Company, MyStore, CompanyPitch, Passport, ActivityAreas, ServiceIndustry, CompanyType

admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(MyStore)
admin.site.register(CompanyPitch)
admin.site.register(Passport)
admin.site.register(ServiceIndustry)
admin.site.register(ActivityAreas)
admin.site.register(CompanyType)
