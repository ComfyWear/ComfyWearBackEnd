"""A module that defines the PredictViewSet class."""
from rest_framework import status, viewsets
from rest_framework.response import Response
from app.models import Prediction
from app.serializers import PredictionSerializer


class PredictViewSet(viewsets.ViewSet):
    """ViewSet for handling Prediction-related operations."""

    def create(self, request):
        """
        Create a new Prediction object.

        :param request: The HTTP request with prediction data.
        :return: Response with created prediction or error.
        """
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
