from django.db import models

from utils.abstract_model import AbstractModel


class Sensor(AbstractModel):
    """
    Represents sensor data in the system.

    This model inherits from the AbstractModel and contains an
    auto-generated UUID as a primary key, fields for local temperature
    and humidity, and a comfort level field.

    :param local_temp: The local temperature reading from the sensor.
    :type local_temp: models.FloatField
    :param local_humid: The local humidity reading from the sensor.
    :type local_humid: models.FloatField

    :return: A string representation of the sensor's UUID.
    :rtype: str
    """

    class Meta:
        """Meta definition for Sensor."""

        app_label = "app"
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"
        ordering = ["id"]

    local_temp = models.FloatField(
        null=True, blank=True, help_text="Local temperature reading"
    )
    local_humid = models.FloatField(
        null=True, blank=True, help_text="Local humidity reading"
    )
