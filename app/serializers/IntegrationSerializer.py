"""The module defines the serializer for the Integration model."""
from rest_framework import serializers

from app.models import Integration


class IntegrationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Integration model.

    Handles the conversion of Integration model instances to JSON format and
    vice versa, simplifying the process of transmitting Task data over APIs.
    """

    class Meta:
        """Meta definition for Task."""

        model = Integration
        fields = "__all__"
