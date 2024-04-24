"""The module defines the Comfort model."""
from django.db import models

from utils.abstract_model import AbstractModel
from app.models.integrate import Integrate


class Comfort(AbstractModel):
    """
    Represents a comfort level descriptor in the system.

    This model inherits from the AbstractModel and contains an
    auto-generated UUID as a primary key, a field for the comfort
    level descriptor, and a foreign key to an associated integration.

    :param comfort: The comfort level descriptor.
    :type comfort: models.CharField
    :param integration: The foreign key to the associated integration.
    :type integration: models.ForeignKey

    :return: A string representation of the comfort level descriptor.
    :rtype: str
    """

    comfort = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Comfort level descriptor"
    )
    integrate = models.ForeignKey(
        Integrate, on_delete=models.CASCADE, related_name='comforts',
        null=True
    )

    class Meta:
        """Meta definition for Comfort."""

        app_label = "app"
        verbose_name = "Comfort"
        verbose_name_plural = "Comforts"
        ordering = ["id"]
