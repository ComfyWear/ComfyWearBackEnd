from django.contrib import admin
from .models import Image, Prediction, Integration, Sensor, Comfort

# Register your models here.
admin.site.register(Image)
admin.site.register(Prediction)
admin.site.register(Integration)
admin.site.register(Sensor)
admin.site.register(Comfort)
