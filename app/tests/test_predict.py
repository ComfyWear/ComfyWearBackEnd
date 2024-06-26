"""This module defines the test suite for the PredictViewSet."""
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from app.tests import BaseTestCase
from app.models import Predict


class PredictViewSetTestCase(BaseTestCase):
    """This class defines the test suite for the PredictViewSet."""

    def test_create_prediction_with_valid_data(self):
        """Test create a prediction object with valid data."""
        with open('app/tests/test_resources/test_image.jpg', 'rb') \
                as image_file:
            data = {
                'secret': self.secret,
                'image': SimpleUploadedFile(image_file.name,
                                            image_file.read()),
            }
            response = self.client.post(self.predict_url, data,
                                        format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Predict.objects.count(), 12)

    def test_create_prediction_with_invalid_secret(self):
        """Test when creating a prediction object with an invalid secret."""
        with open('app/tests/test_resources/test_image.jpg', 'rb') \
                as image_file:
            data = {
                'secret': 'invalid_secret',
                'image': SimpleUploadedFile(image_file.name,
                                            image_file.read()),
            }
            response = self.client.post(self.predict_url, data,
                                        format='multipart')
            self.assertEqual(response.status_code,
                             status.HTTP_201_CREATED)

    def test_create_prediction_with_missing_image(self):
        """Test when creating a prediction object with missing image."""
        data = {
            'secret': self.secret,
        }
        response = self.client.post(self.predict_url, data,
                                    format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing required data')

    def test_create_prediction_with_invalid_format(self):
        """Test when creating a prediction object with an invalid format."""
        with open('app/tests/test_resources/test_invalid_image.txt', 'rb') \
                as invalid_image_file:
            data = {
                'secret': self.secret,
                'image': SimpleUploadedFile(invalid_image_file.name,
                                            invalid_image_file.read()),
            }
            response = self.client.post(self.predict_url, data,
                                        format='multipart')
            self.assertEqual(response.status_code,
                             status.HTTP_400_BAD_REQUEST)
            self.assertIn('error', response.data)
