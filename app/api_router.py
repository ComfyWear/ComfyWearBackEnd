"""A module that defines the URL configuration for the app."""
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from app.views import PredictViewSet, SensorViewSet, \
    ComfortViewSet, IntegrateViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("predict", PredictViewSet, basename="predict")
router.register("sensor", SensorViewSet, basename="sensor")
router.register("comfort", ComfortViewSet, basename="comfort")
router.register("integrate", IntegrateViewSet, basename="integrate")

app_name = "api"
urlpatterns = router.urls
