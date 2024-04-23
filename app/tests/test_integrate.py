"""This module defines the test suite for the IntegrationViewSet."""
from rest_framework import status

from app.models import Comfort, Sensor, Prediction, Integrate
from app.tests import BaseTestCase


class IntegrationViewSetTestCase(BaseTestCase):
    """This class defines the test suite for the IntegrationViewSet."""

    def setUp(self):
        """Define the test client and other test variables."""
        super().setUp()
        self.maxDiff = None
        self.integration = Integrate.objects.create()

        self.comfort1 = Comfort.objects.create(
            comfort="1",
            integration=self.integration,
            timestamp='2023-06-01T10:00:00Z')
        self.comfort2 = Comfort.objects.create(
            comfort="2",
            integration=self.integration,
            timestamp='2023-06-01T11:00:00Z')
        self.comfort3 = Comfort.objects.create(
            comfort="3",
            integration=self.integration,
            timestamp='2023-06-01T12:00:00Z')
        self.comfort4 = Comfort.objects.create(
            comfort="4",
            integration=self.integration,
            timestamp='2023-06-01T13:00:00Z')

        self.sensor1 = Sensor.objects.create(local_temp=25.5,
                                             local_humid=60,
                                             integration=self.integration)
        self.sensor2 = Sensor.objects.create(local_temp=26.0,
                                             local_humid=65.0,
                                             integration=self.integration)

        self.prediction1 = Prediction.objects.create(
            predicted_upper='T-shirt',
            predicted_lower='Shorts',
            integration=self.integration,
            timestamp='2023-06-01T10:00:00Z')
        self.prediction2 = Prediction.objects.create(
            predicted_upper='Jacket',
            predicted_lower='Jeans',
            integration=self.integration,
            timestamp='2023-06-01T11:00:00Z')

    def test_list_comfort_data(self):
        """
        Test the API can list all comfort data.

        The API should return the average comfort level,
        comfort level distribution, comfort level details,
        and clothing label counts.
        """
        response = self.client.get(self.integrate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'avg_comfort_level': 2.5,
            'comfort_level_distribution': [
                {'comfort': "1", 'count': 1},
                {'comfort': "2", 'count': 1},
                {'comfort': "3", 'count': 1},
                {'comfort': "4", 'count': 1}
            ],
            'comfort_level_details': {
                "1": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {'T-shirt': 1},
                    'lower_labels': {'Shorts': 1}
                },
                "2": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {'Jacket': 1},
                    'lower_labels': {'Jeans': 1}
                },
                "3": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {None: 1},
                    'lower_labels': {None: 1}
                },
                "4": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {None: 1},
                    'lower_labels': {None: 1}
                }
            },
            'label_counts': {
                'T-shirt': 1,
                'Shorts': 1,
                'Jacket': 1,
                'Jeans': 1
            }
        }

        self.assertEqual(response.data, expected_data)

    def test_list_comfort_data_empty(self):
        """
        Test the API can list all comfort data when there is no data.

        The API should return None for the average comfort level
        and empty lists for the comfort level distribution,
        comfort level details, and clothing label counts.
        """
        Comfort.objects.all().delete()
        response = self.client.get(self.integrate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'avg_comfort_level': None,
            'comfort_level_distribution': [],
            'comfort_level_details': {},
            'label_counts': {}
        }

        self.assertEqual(response.data, expected_data)

    def test_list_comfort_data_no_predictions(self):
        """
        Test the API can list all comfort data when there are no predictions.

        The API should return the average comfort level,
        comfort level distribution, and comfort level details,
        but the clothing label counts should be empty.
        """
        Prediction.objects.all().delete()
        response = self.client.get(self.integrate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'avg_comfort_level': 2.5,
            'comfort_level_distribution': [
                {'comfort': "1", 'count': 1},
                {'comfort': "2", 'count': 1},
                {'comfort': "3", 'count': 1},
                {'comfort': "4", 'count': 1}
            ],
            'comfort_level_details': {
                "1": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {None: 1},
                    'lower_labels': {None: 1}
                },
                "2": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {None: 1},
                    'lower_labels': {None: 1}
                },
                "3": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {None: 1},
                    'lower_labels': {None: 1}
                },
                "4": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {None: 1},
                    'lower_labels': {None: 1}
                }
            },
            'label_counts': {}
        }

        self.assertEqual(response.data, expected_data)

    def test_list_comfort_data_no_sensors(self):
        """
        Test the API can list all comfort data when there are no sensors.

        The API should return None for the average comfort level and
        empty lists for the comfort level distribution,
        comfort level details, and clothing label counts.
        """
        Sensor.objects.all().delete()
        response = self.client.get(self.integrate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'avg_comfort_level': 2.5,
            'comfort_level_distribution': [
                {'comfort': "1", 'count': 1},
                {'comfort': "2", 'count': 1},
                {'comfort': "3", 'count': 1},
                {'comfort': "4", 'count': 1}
            ],
            'comfort_level_details': {
                "1": {
                    'count': 1,
                    'avg_temp': 0,
                    'avg_humid': 0,
                    'upper_labels': {'T-shirt': 1},
                    'lower_labels': {'Shorts': 1}
                },
                "2": {
                    'count': 1,
                    'avg_temp': 0,
                    'avg_humid': 0,
                    'upper_labels': {'Jacket': 1},
                    'lower_labels': {'Jeans': 1}
                },
                "3": {
                    'count': 1,
                    'avg_temp': 0,
                    'avg_humid': 0,
                    'upper_labels': {None: 1},
                    'lower_labels': {None: 1}
                },
                "4": {
                    'count': 1,
                    'avg_temp': 0,
                    'avg_humid': 0,
                    'upper_labels': {None: 1},
                    'lower_labels': {None: 1}
                }
            },
            'label_counts': {
                'T-shirt': 1,
                'Shorts': 1,
                'Jacket': 1,
                'Jeans': 1
            }
        }

        self.assertEqual(response.data, expected_data)

    def test_comfort_level_distribution_all(self):
        """
        Test retrieve the comfort level distribution for all comfort levels.

        The API should return the comfort level distribution
        based on all available comfort data.
        """
        response = self.client.get(self.comfort_level_distribution_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'comfort_level_distribution': [
                {'comfort': "1", 'count': 1},
                {'comfort': "2", 'count': 1},
                {'comfort': "3", 'count': 1},
                {'comfort': "4", 'count': 1}
            ]
        }

        self.assertEqual(response.data, expected_data)

    def test_comfort_level_distribution_specific(self):
        """
        Test retrieve the comfort level distribution for a specific level.

        The API should return the comfort level distribution
        for the specified comfort level.
        """
        comfort_level = 2
        url = f"{self.comfort_level_distribution_url}{comfort_level}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'comfort_level_distribution': [
                {'comfort': "2", 'count': 1}
            ]
        }

        self.assertEqual(response.data, expected_data)

    def test_comfort_level_details_all(self):
        """
        Test retrieve the comfort level details for all comfort levels.

        The API should return the comfort level details
        based on all available comfort data.
        """
        response = self.client.get(self.comfort_level_details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'comfort_level_details': {
                "1": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {'T-shirt': 1},
                    'lower_labels': {'Shorts': 1}
                },
                "2": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {'Jacket': 1},
                    'lower_labels': {'Jeans': 1}
                },
                "3": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {None: 1},
                    'lower_labels': {None: 1}
                },
                "4": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {None: 1},
                    'lower_labels': {None: 1}
                }
            }
        }

        self.assertEqual(response.data, expected_data)

    def test_comfort_level_details_specific(self):
        """
        Test retrieve the comfort level details for a specific comfort level.

        The API should return the comfort level details
        for the specified comfort level.
        """
        comfort_level = 1
        url = f"{self.comfort_level_details_url}{comfort_level}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'comfort_level_details': {
                "1": {
                    'count': 1,
                    'avg_temp': 25.75,
                    'avg_humid': 62.5,
                    'upper_labels': {'T-shirt': 1},
                    'lower_labels': {'Shorts': 1}
                }
            }
        }

        self.assertEqual(response.data, expected_data)

    def test_label_counts_all(self):
        """
        Test the API can retrieve the clothing label counts for all labels.

        The API should return the counts of each clothing label
        based on all available prediction data.
        """
        response = self.client.get(self.label_counts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'label_counts': {
                'T-shirt': 1,
                'Shorts': 1,
                'Jacket': 1,
                'Jeans': 1
            }
        }

        self.assertEqual(response.data, expected_data)

    def test_label_counts_specific(self):
        """
        Test the API can retrieve the count for a specific clothing label.

        The API should return the count for the specified clothing label
        based on all available prediction data.
        """
        label = 'T-shirt'
        url = f"{self.label_counts_url}{label}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'T-shirt': 1
        }

        self.assertEqual(response.data, expected_data)
