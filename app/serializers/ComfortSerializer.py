"""The module defines the serializer for the Comfort model."""
from rest_framework import serializers
from app.models import Comfort


class ComfortSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comfort model.

    Handles the conversion of Comfort model instances to JSON format and
    vice versa, simplifying the process of transmitting Task data over APIs.
    """

    class Meta:
        """Meta definition for Task."""

        model = Comfort
        fields = "__all__"
