"""Abstract model classes for generate unique id for each model."""
import uuid

from django.db import models
from django.utils import timezone


class AbstractModel(models.Model):
    """Abstract model class for generate unique id for each model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        """Meta definition for Model."""

        abstract = True

    def __str__(self):
        """Unicode representation of Model."""
        return str(self.id)
