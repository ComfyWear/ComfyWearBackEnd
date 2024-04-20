"""A module that defines the URL configuration for the app."""
from django.urls import include, path

urlpatterns = [
    path("api/", include("app.api_router")),
]
