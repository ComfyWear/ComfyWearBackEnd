"""The module defines the serializer for the Image model."""
from rest_framework import serializers
from app.models import Image


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Image model.

    Handles the conversion of Image model instances to JSON format and
    vice versa, simplifying the process of transmitting Task data over APIs.
    """
    detected_image = serializers.ImageField(use_url=True)

    class Meta:
        """Meta definition for Task."""

        model = Image
        fields = "__all__"
