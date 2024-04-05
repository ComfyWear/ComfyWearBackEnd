from django.db import models

from utils.abstract_model import AbstractModel
from app.models.integration import Integration


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
    predicted_type = models.CharField(
        max_length=255, null=True, blank=True, help_text="Type of the predicted object"
    )
    integration = models.ForeignKey(
        Integration, on_delete=models.CASCADE, related_name='predictions', null=True
    )

    class Meta:
        app_label = "app"
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"
        ordering = ["id"]
