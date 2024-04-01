from django.db import models

from utils.abstract_model import AbstractModel


class Integration(AbstractModel):
    """
    Represents integrated data that combines sensor readings, predictions,
    and images within the system.

    This model inherits from the AbstractModel and contains an auto-generated
    UUID as a primary key and foreign keys to the Sensor, Prediction, and Image models.

    :param sensor: The associated sensor data.
    :type sensor: models.ForeignKey
    :param prediction: The associated prediction data.
    :type prediction: models.ForeignKey
    :param image: The associated image data.
    :type image: models.ForeignKey

    :return: A string representation of the integrated data UUID.
    :rtype: str
    """

    class Meta:
        """Meta definition for Integration."""
        app_label = "app"
        verbose_name = "Integration"
        verbose_name_plural = "Integrations"
        ordering = ["id"]

    sensor = models.ForeignKey(
        'Sensor', on_delete=models.CASCADE, related_name='integrations'
    )
    prediction = models.ForeignKey(
        'Prediction', on_delete=models.CASCADE, related_name='integrations'
    )
    image = models.ForeignKey(
        'Image', on_delete=models.CASCADE, related_name='integrations'
    )
