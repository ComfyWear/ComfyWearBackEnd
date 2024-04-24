"""The module defines the Prediction model."""
from django.db import models

from utils.abstract_model import AbstractModel
from app.models.integrate import Integrate


class Prediction(AbstractModel):
    """
    Represents a prediction in the system.

    This model inherits from the AbstractModel and contains an
    auto-generated UUID as a primary key, a field for the type of
    prediction, and a foreign key to an associated image.

    :param predicted_type: The type of object predicted.
    :type predicted_type: models.CharField
    :param integration: The foreign key to the associated integration.
    :type integration: models.ForeignKey

    :return: A string representation of the prediction type.
    :rtype: str
    """

    predicted_upper = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Upper of the predicted object"
    )
    predicted_lower = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Lower of the predicted object"
    )
    integrate = models.ForeignKey(
        Integrate, on_delete=models.CASCADE,
        related_name='predictions', null=True
    )

    class Meta:
        """Meta definition for Prediction."""

        app_label = "app"
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"
        ordering = ["id"]
