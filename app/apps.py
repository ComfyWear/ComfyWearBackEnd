"""A module that defines the URL configuration for the app."""
from django.apps import AppConfig


class AppConfig(AppConfig):
    """AppConfig class."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
