"""A module that defines the SensorViewSet class."""
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from app.serializers import SensorSerializer
from app.models import Integrate


class SensorViewSet(viewsets.ViewSet):
    """ViewSet for handling Sensor-related operations."""

    parser_classes = (MultiPartParser, FormParser)

    def create(self, request):
        """
        Create a new Sensor object for a specific integrate.

        :param request: The HTTP request with task data.
        :return: Response with created task or error.
        """
        secret = request.data.get('secret')
        local_temp = request.data.get('local_temp')
        local_humid = request.data.get('local_humid')

        if secret and local_temp and local_humid:
            integrate = Integrate.objects.filter(secret=secret).first()

            if not integrate:
                integrate = Integrate.objects.create(secret=secret)

            serializer = SensorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(integrate=integrate)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid request data.'},
                        status=status.HTTP_400_BAD_REQUEST)
