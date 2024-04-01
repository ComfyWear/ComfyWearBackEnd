from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from app.views import PredictViewSet, SensorViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("predict", PredictViewSet, basename="predict")
router.register("sensor", SensorViewSet, basename="sensor")

app_name = "api"
urlpatterns = router.urls
