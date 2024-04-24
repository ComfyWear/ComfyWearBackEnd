"""A module that defines the ComfortViewSet class."""
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from app.serializers import ComfortSerializer
from app.models import Integrate, Comfort


class ComfortViewSet(viewsets.ViewSet):
    """ViewSet for handling Comfort-related operations."""

    parser_classes = (MultiPartParser, FormParser)

    def create(self, request):
        """
        Create a new Comfort object for a specific integrate.

        :param request: The HTTP request with prediction data.
        :return: Response with created prediction or error.
        """
        secret = request.data.get('secret')
        comfort = request.data.get('comfort')
        integrate = Integrate.objects.filter(secret=secret).first()

        if integrate and comfort:
            serializer = ComfortSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(integrate=integrate)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid secret code'},
                        status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific Comfort object.

        :param request: The HTTP request.
        :type request: rest_framework.request.Request
        :param pk: The primary key of the Comfort object.
        :type pk: int
        :return: The HTTP response with the Comfort object.
        :rtype: rest_framework.response.Response
        """
        try:
            comfort = Comfort.objects.get(pk=pk)
            serializer = ComfortSerializer(comfort)
            return Response(serializer.data)
        except Comfort.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
