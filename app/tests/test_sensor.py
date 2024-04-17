from app.models import Sensor
from app.tests import BaseTestCase
from rest_framework import status


class SensorViewSetTestCase(BaseTestCase):
    """This class defines the test suite for the SensorViewSet."""

    def test_create_sensor_with_valid_data(self):
        """Test the API can create a sensor object with valid data."""
        data = {
            'secret': self.secret,
            'local_temp': 25.5,
            'local_humid': 60.0
        }
        response = self.client.post(self.sensor_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sensor.objects.count(), 1)
        self.assertEqual(Sensor.objects.get().local_temp, 25.5)
        self.assertEqual(Sensor.objects.get().local_humid, 60.0)
        self.assertEqual(Sensor.objects.get().integration, self.integration)

    def test_create_sensor_with_invalid_secret(self):
        """Test the API returns an error when creating a sensor object with an invalid secret."""
        data = {
            'secret': 'invalid_secret',
            'local_temp': 25.5,
            'local_humid': 60.0
        }
        response = self.client.post(self.sensor_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sensor.objects.count(), 1)
        self.assertEqual(Sensor.objects.get().local_temp, 25.5)
        self.assertEqual(Sensor.objects.get().local_humid, 60.0)
        self.assertEqual(Sensor.objects.get().integration.secret == 'invalid_secret', True)

    def test_create_sensor_with_missing_data(self):
        """Test the API returns an error when creating a sensor object with missing data."""
        data = {
            'secret': self.secret,
            'local_temp': 25.5
        }
        response = self.client.post(self.sensor_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sensor.objects.count(), 0)
