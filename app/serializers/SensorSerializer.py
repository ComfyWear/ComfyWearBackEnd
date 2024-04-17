"""The module defines the serializer for the Sensor model."""
from rest_framework import serializers
from app.models import Sensor


class SensorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Sensor model.

    Handles the conversion of Sensor model instances to JSON format and
    vice versa, simplifying the process of transmitting Task data over APIs.
    """

    class Meta:
        """Meta definition for Task."""

        model = Sensor
        fields = "__all__"
