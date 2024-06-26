"""The module defines the Image model."""
from django.db import models

from utils.abstract_model import AbstractModel
from app.models.integrate import Integrate


class Image(AbstractModel):
    """
    Represents an image in the system.

    This model inherits from the AbstractModel and contains an
    auto-generated UUID as a primary key and an image field
    for storing detected images.

    :param detected_image: The field for storing the uploaded image.
    :type detected_image: models.ImageField
    :param integrate: The foreign key to the associated integrate.
    :type integrate: models.ForeignKey

    :return: A string representation of the image UUID.
    :rtype: str
    """

    detected_image = models.ImageField(
        upload_to='detected_images/', null=True, blank=True
    )
    integrate = models.ForeignKey(
        Integrate, on_delete=models.CASCADE, related_name='images', null=True
    )

    class Meta:
        """Meta definition for Image."""

        app_label = "app"
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ["id"]
