"""A module that defines the ComfortViewSet class."""
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from app.serializers import ComfortSerializer
from app.models import Integration


class ComfortViewSet(viewsets.ViewSet):
    """ViewSet for handling Comfort-related operations."""
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request):
        """
        Create a new Comfort object for a specific integration.

        :param request: The HTTP request with prediction data.
        :return: Response with created prediction or error.
        """
        secret = request.data.get('secret')
        comfort = request.data.get('comfort')
        integration = Integration.objects.filter(secret=secret).first()

        if integration and comfort:
            serializer = ComfortSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(integration=integration)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid secret code'},
                        status=status.HTTP_400_BAD_REQUEST)
