"""A module that defines the URL configuration for the app."""
from django.contrib import admin
from .models import Image, Prediction, Integrate, Sensor, Comfort

admin.site.register(Image)
admin.site.register(Prediction)
admin.site.register(Integrate)
admin.site.register(Sensor)
admin.site.register(Comfort)
