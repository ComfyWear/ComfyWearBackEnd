"""A module that defines the URL configuration for the app."""
from django.contrib import admin
from .models import Image, Prediction, Integration, Sensor, Comfort

admin.site.register(Image)
admin.site.register(Prediction)
admin.site.register(Integration)
admin.site.register(Sensor)
admin.site.register(Comfort)
