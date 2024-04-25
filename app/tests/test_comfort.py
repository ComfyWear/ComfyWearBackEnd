"""This module defines the test suite for the IntegratViewSet."""
from rest_framework import status

from app.models import Comfort
from app.tests import BaseTestCase


class ComfortViewSetTestCase(BaseTestCase):
    """This class defines the test suite for the ComfortViewSet."""

    def test_create_comfort_with_valid_data(self):
        """Test the API can create a comfort object with valid data."""
        data = {
            'secret': self.secret,
            'comfort': 'Comfortable'
        }
        response = self.client.post(self.comfort_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comfort.objects.count(), 1)
        self.assertEqual(Comfort.objects.get().comfort, 'Comfortable')
        self.assertEqual(Comfort.objects.get().integrate, self.integrate)

    def test_create_comfort_with_invalid_secret(self):
        """Test when creating a comfort object with an invalid secret."""
        data = {
            'secret': 'invalid_secret',
            'comfort': 'Comfortable'
        }
        response = self.client.post(self.comfort_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comfort.objects.count(), 0)
        self.assertEqual(response.data['error'], 'Invalid secret code or comfort values')

    def test_create_comfort_with_missing_comfort_data(self):
        """Test when creating a comfort object with missing comfort data."""
        data = {
            'secret': self.secret,
        }
        response = self.client.post(self.comfort_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comfort.objects.count(), 0)
