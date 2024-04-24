# api_router.py
"""A module that defines the URL configuration for the app."""
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from app.views import PredictViewSet, SensorViewSet, ComfortViewSet, \
    IntegrateViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("predict", PredictViewSet, basename="predict")
router.register("sensor", SensorViewSet, basename="sensor")
router.register("comfort", ComfortViewSet, basename="comfort")
router.register("integrate", IntegrateViewSet, basename="integrate")

urlpatterns = [
    *router.urls,
    path('integrate/avg-comfort-level/',
         IntegrateViewSet.as_view({'get': 'avg_comfort_level'}),
         name='avg-comfort-level-detail'),
    path('integrate/comfort-level-distribution/',
         IntegrateViewSet.as_view({'get': 'comfort_level_distribution'}),
         name='comfort-level-distribution'),
    path('integrate/comfort-level-distribution/<int:comfort>/',
         IntegrateViewSet.as_view({'get': 'comfort_level_distribution'}),
         name='comfort-level-distribution-detail'),
    path('integrate/comfort-level-details/',
         IntegrateViewSet.as_view({'get': 'comfort_level_details'}),
         name='comfort-level-details'),
    path('integrate/comfort-level-details/<int:comfort>/',
         IntegrateViewSet.as_view({'get': 'comfort_level_details'}),
         name='comfort-level-details-detail'),
    path('integrate/label-counts/',
         IntegrateViewSet.as_view({'get': 'label_counts'}),
         name='label-counts'),
    path('integrate/label-counts/<str:label>/',
         IntegrateViewSet.as_view({'get': 'label_counts'}),
         name='label-count-detail'),
    path('integrate/correlation/',
         IntegrateViewSet.as_view({'get': 'correlation'}),
         name='correlation'),
]
