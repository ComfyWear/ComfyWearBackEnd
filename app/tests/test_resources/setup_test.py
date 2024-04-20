"""This module defines the test suite for the IntegrationViewSet."""
from rest_framework.test import APIClient, APITestCase

from app.models import Integration


class BaseTestCase(APITestCase):
    """This class defines the base test suite."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.secret = 'test_secret'
        self.integration = Integration.objects.create(secret=self.secret)

        self.comfort_url = "/app/api/comfort/"
        self.sensor_url = "/app/api/sensor/"
        self.predict_url = "/app/api/predict/"
        self.integrate_url = "/app/api/integrate/"
        self.comfort_level_distribution_url = "/app/api/integrate/comfort-level-distribution/"
        self.comfort_level_details_url = "/app/api/integrate/comfort-level-details/"
        self.label_counts_url = "/app/api/integrate/label-counts/"

        self.client = APIClient()
