from django.contrib import admin
from .models import AdditionalService, TrainingModule, VideoTraining, ContactUs

admin.site.register(AdditionalService)
admin.site.register(TrainingModule)
admin.site.register(VideoTraining)
admin.site.register(ContactUs)