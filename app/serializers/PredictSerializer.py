"""The module defines the serializer for the Prediction model."""
from rest_framework import serializers

from app.models import Predict


class PredictSerializer(serializers.ModelSerializer):
    """
    Serializer for the Prediction model.

    Handles the conversion of Prediction model instances to JSON format and
    vice versa, simplifying the process of transmitting Task data over APIs.
    """

    class Meta:
        """Meta definition for Task."""

        model = Predict
        fields = "__all__"
