"""The module defines the Sensor model."""""
from django.db import models

from utils.abstract_model import AbstractModel
from app.models.integrate import Integrate


class Sensor(AbstractModel):
    """
    Represents a sensor in the system.

    This model inherits from the AbstractModel and contains an
    auto-generated UUID as a primary key, fields for local temperature
    and humidity readings, and a foreign key to an associated integration.

    :param local_temp: The local temperature reading.
    :type local_temp: models.FloatField
    :param local_humid: The local humidity reading.
    :type local_humid: models.FloatField
    :param integration: The foreign key to the associated integration.
    :type integration: models.ForeignKey

    :return: A string representation of the sensor UUID.
    :rtype: str
    """

    local_temp = models.FloatField(
        null=True, blank=True, help_text="Local temperature reading"
    )
    local_humid = models.FloatField(
        null=True, blank=True, help_text="Local humidity reading"
    )
    integrate = models.ForeignKey(
        Integrate, on_delete=models.CASCADE, related_name='sensors',
        null=True
    )

    class Meta:
        """Meta definition for Sensor."""

        app_label = "app"
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"
        ordering = ["id"]
