"""The module defines the serializer for the Prediction model."""
from rest_framework import serializers
from app.models import Prediction


class PredictionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Prediction model.

    Handles the conversion of Prediction model instances to JSON format and
    vice versa, simplifying the process of transmitting Task data over APIs.
    """
    image = serializers.ImageField(required=False)

    class Meta:
        """Meta definition for Task."""

        model = Prediction
        fields = "__all__"
