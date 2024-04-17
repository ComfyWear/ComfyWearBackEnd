"""The module defines the PredictViewSet class."""
from django.db import models
from utils.abstract_model import AbstractModel


class Integration(AbstractModel):
    """
    Represents a collection of related data for a particular integration
    within the system.

    This model inherits from the AbstractModel and contains an auto-generated
    UUID as a primary key.

    :return: A string representation of the integration's UUID.
    :rtype: str
    """

    secret = models.CharField(
        max_length=255, null=True, blank=True, help_text="Secrete integrate code"
    )

    class Meta:
        """Meta definition for Integration."""
        app_label = "app"
        verbose_name = "Integration"
        verbose_name_plural = "Integrations"
        ordering = ["id"]
