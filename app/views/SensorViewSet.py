"""A module that defines the SensorViewSet class."""
from rest_framework import status, viewsets
from rest_framework.response import Response
from app.serializers import SensorSerializer


class SensorViewSet(viewsets.ViewSet):
    """ViewSet for handling Sensor-related operations."""

    def create(self, request):
        """
        Create a new Sensor object for a specific user.

        :param request: The HTTP request with task data.
        :return: Response with created task or error.
        """

        data = request.data
        serializer = SensorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
