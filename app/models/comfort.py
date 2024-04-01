from django.db import models

from utils.abstract_model import AbstractModel


class Comfort(AbstractModel):
    """
    Represents sensor data in the system.

    This model inherits from the AbstractModel and contains an
    auto-generated UUID as a primary key, fields for local temperature
    and humidity, and a comfort level field.

    :param comfort: A string representing the comfort level based on the sensor data.
    :type comfort: models.CharField

    :return: A string representation of the sensor's UUID.
    :rtype: str
    """

    class Meta:
        """Meta definition for Comfort."""

        app_label = "app"
        verbose_name = "Comfort"
        verbose_name_plural = "Comforts"
        ordering = ["id"]

    comfort = models.CharField(
        max_length=255, null=True, blank=True, help_text="Comfort level descriptor"
    )
