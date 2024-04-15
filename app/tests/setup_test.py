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

        self.client = APIClient()
