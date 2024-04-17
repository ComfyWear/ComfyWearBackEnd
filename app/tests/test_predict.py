"""This module defines the test suite for the PredictViewSet."""
from app.models import Prediction
from app.tests import BaseTestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


class PredictViewSetTestCase(BaseTestCase):
    """This class defines the test suite for the PredictViewSet."""

    def test_create_prediction_with_valid_data(self):
        """Test the API can create a prediction object with valid data."""
        with open('app/tests/resources/test_image.jpg', 'rb') as image_file:
            data = {
                'secret': self.secret,
                'image': SimpleUploadedFile(image_file.name,
                                            image_file.read()),
            }
            response = self.client.post(self.predict_url, data,
                                        format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Prediction.objects.count(), 12)

    def test_create_prediction_with_invalid_secret(self):
        """Test the API returns an error when creating a prediction object with an invalid secret."""
        with open('app/tests/resources/test_image.jpg', 'rb') as image_file:
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
        """Test the API returns an error when creating a prediction object with missing image."""
        data = {
            'secret': self.secret,
        }
        response = self.client.post(self.predict_url, data,
                                    format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing required data')

    def test_create_prediction_with_invalid_format(self):
        """Test the API returns an error when creating a prediction object with an invalid image format."""
        with open('app/tests/resources/test_invalid_image.txt', 'rb') \
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
