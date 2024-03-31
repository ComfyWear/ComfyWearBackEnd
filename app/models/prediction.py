from django.db import models
import uuid

from utils.abstract_model import AbstractModel


class Prediction(AbstractModel):
    """
    Represents a prediction in the system.

    This model inherits from the AbstractModel and contains an
    auto-generated UUID as a primary key, a field for the type of
    prediction, and a foreign key to an associated image.

    :param id: The UUID of the prediction, auto-generated upon creation.
    :type id: models.UUIDField
    :param predicted_type: The type of object predicted.
    :type predicted_type: models.CharField
    :param image: A foreign key that links to an image that the prediction is associated with.
    :type image: models.ForeignKey

    :return: A string representation of the prediction type.
    :rtype: str
    """

    class Meta:
        """Meta definition for Prediction."""

        app_label = "app"
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"
        ordering = ["id"]

    predicted_type = models.CharField(
        max_length=255, null=True, blank=True, help_text="Type of the predicted object"
    )
    image = models.ForeignKey(
        'Image', on_delete=models.CASCADE, related_name='predictions'
    )
