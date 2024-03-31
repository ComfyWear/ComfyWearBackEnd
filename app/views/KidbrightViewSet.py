"""A module that defines the KidbrightViewSet class."""
from rest_framework import viewsets


class KidbrightViewSet(viewsets.ViewSet):
    """ViewSet for handling Kidbright-related operations."""

    def create(self, request):
        """
        Create a new Kidbright object.

        :param request: The HTTP request with Kidbright data.
        :return: Response with created Kidbright object or error.
        """
        pass
