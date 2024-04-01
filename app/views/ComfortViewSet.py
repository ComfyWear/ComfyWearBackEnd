"""A module that defines the ComfortViewSet class."""
from rest_framework import status, viewsets
from rest_framework.response import Response
from app.serializers import ComfortSerializer


class ComfortViewSet(viewsets.ViewSet):
    """ViewSet for handling Comfort-related operations."""

    def create(self, request):
        """
        Create a new Comfort object.

        :param request: The HTTP request with prediction data.
        :return: Response with created prediction or error.
        """
        serializer = ComfortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
