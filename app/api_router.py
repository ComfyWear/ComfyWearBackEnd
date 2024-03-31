from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from app.views import PredictViewSet, KidbrightViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("predict", PredictViewSet, basename="predict")
router.register("sensor", KidbrightViewSet, basename="sensor")

app_name = "api"
urlpatterns = router.urls
