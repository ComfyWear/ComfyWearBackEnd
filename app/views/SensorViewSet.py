"""A module that defines the SensorViewSet class."""
from rest_framework import status, viewsets
from rest_framework.response import Response
from app.serializers import SensorSerializer
from app.models import Integration
from rest_framework.parsers import MultiPartParser, FormParser


class SensorViewSet(viewsets.ViewSet):
    """ViewSet for handling Sensor-related operations."""
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request):
        """
        Create a new Sensor object for a specific integration.

        :param request: The HTTP request with task data.
        :return: Response with created task or error.
        """
        secret = request.data.get('secret')
        integration = Integration.objects.filter(secret=secret).first()

        if integration:
            serializer = SensorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(integration=integration)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid secret code'},
                            status=status.HTTP_400_BAD_REQUEST)