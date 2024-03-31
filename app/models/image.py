from django.db import models


from utils.abstract_model import AbstractModel


class Image(AbstractModel):
    """
    Represents an image in the system.

    This model inherits from the AbstractModel and contains an
    auto-generated UUID as a primary key and an image field
    for storing detected images.

    :param id: The UUID of the image, auto-generated upon creation.
    :type id: models.UUIDField
    :param detected_image: The field for storing the uploaded image.
    :type detected_image: models.ImageField

    :return: A string representation of the image UUID.
    :rtype: str
    """

    class Meta:
        """Meta definition for Image."""

        app_label = "app"
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ["id"]

    detected_image = models.ImageField(
        upload_to='detected_images/', null=True, blank=True
    )
