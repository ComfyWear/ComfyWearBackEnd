"""The module defines the IntegrationViewSet class."""
from typing import Dict, List

from django.db.models import Avg, Count
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
import pandas as pd

from app.models import Comfort, Sensor, Prediction


class IntegrateViewSet(viewsets.ViewSet):
    """
    ViewSet for handling Integration-related operations.

    This ViewSet provides a list of all comfort data,
    including the average comfort level, comfort level distribution,
    comfort level details, and clothing label counts.
    """

    def list(self, request: Request) -> Response:
        """
        List all comfort data.

        :param request: The HTTP request.
        :type request: rest_framework.request.Request
        :return: The HTTP response containing the comfort data.
        :rtype: rest_framework.response.Response
        """
        comfort_data = Comfort.objects.all().order_by("timestamp")

        if comfort_data.exists():
            avg_comfort_level = self._get_average_comfort_level(comfort_data)
            comfort_level_distribution = self._get_comfort_level_distribution(
                comfort_data)
            integrate_data = self._group_data_by_integrate(comfort_data)
            comfort_level_details = self._get_comfort_level_details(
                integrate_data)
            label_counts = self._get_label_counts()

            response_data = {
                'avg_comfort_level': avg_comfort_level,
                'comfort_level_distribution': comfort_level_distribution,
                'comfort_level_details': comfort_level_details,
                'label_counts': label_counts
            }
        else:
            response_data = {
                'avg_comfort_level': None,
                'comfort_level_distribution': [],
                'comfort_level_details': {},
                'label_counts': {}
            }

        return Response(response_data)

    def avg_comfort_level(self, request: Request) -> Response:
        """
        Get the average comfort level.

        :param request: The HTTP request.
        :type request: rest_framework.request.Request
        :return: The average comfort level.
        :rtype: rest_framework.response.Response
        """
        comfort_data = Comfort.objects.all().order_by("timestamp")
        avg_comfort_level = self._get_average_comfort_level(comfort_data)
        return Response({'avg_comfort_level': avg_comfort_level})

    def comfort_level_distribution(self, request: Request,
                                   comfort: int = None) -> Response:
        """
        Get the comfort level distribution.

        :param request: The HTTP request.
        :type request: rest_framework.request.Request
        :param comfort: Optional comfort level to filter the distribution.
        :type comfort: int, optional
        :return: The comfort level distribution.
        :rtype: rest_framework.response.Response
        """
        comfort_data = Comfort.objects.all().order_by("timestamp")
        if comfort:
            comfort_data = comfort_data.filter(comfort=comfort)
        comfort_level_distribution = self._get_comfort_level_distribution(
            comfort_data)
        return Response(
            {'comfort_level_distribution': comfort_level_distribution})

    def comfort_level_details(self, request: Request,
                              comfort: int = None) -> Response:
        """
        Get the comfort level details.

        :param request: The HTTP request.
        :type request: rest_framework.request.Request
        :param comfort: Optional comfort level to filter the details.
        :type comfort: int, optional
        :return: The comfort level details.
        :rtype: rest_framework.response.Response
        """
        comfort_data = Comfort.objects.all().order_by("timestamp")
        if comfort:
            comfort_data = comfort_data.filter(comfort=comfort)
        integrate_data = self._group_data_by_integrate(comfort_data)
        comfort_level_details = self._get_comfort_level_details(
            integrate_data)
        return Response({'comfort_level_details': comfort_level_details})

    def label_counts(self, request: Request, label: str = None) -> Response:
        """
        Get the clothing label counts.

        :param request: The HTTP request.
        :type request: rest_framework.request.Request
        :param label: Optional label to get the count for.
        :type label: str, optional
        :return: The clothing label counts or count for a specific label.
        :rtype: rest_framework.response.Response
        """
        label_counts = self._get_label_counts()
        if label:
            count = label_counts.get(label, 0)
            return Response({label: count})
        else:
            return Response({'label_counts': label_counts})

    def correlation(self, request: Request) -> Response:
        """
        Get the raw data for local temperature, local humidity, and comfort level.

        :param request: The HTTP request.
        :type request: rest_framework.request.Request
        :return: The raw data for plotting.
        :rtype: rest_framework.response.Response
        """
        comfort_data = Comfort.objects.all().order_by("timestamp")
        sensor_data = Sensor.objects.all().order_by("timestamp")

        data = []

        for comfort in comfort_data:
            integrate = comfort.integrate
            comfort_level = comfort.comfort

            try:
                sensor = sensor_data.filter(
                    integrate=comfort.integrate).latest('timestamp')

                local_temp = sensor.local_temp
                local_humid = sensor.local_humid

                print(1)

                data.append({
                    'local_temp': local_temp,
                    'local_humid': local_humid,
                    'comfort_level': comfort_level
                })
            except Sensor.DoesNotExist:
                pass

        response_data = {
            'data': data
        }

        return Response(response_data)

    def _get_average_comfort_level(self, comfort_data: Comfort) -> float:
        """
        Get the average comfort level.

        :param comfort_data: The comfort data queryset.
        :type comfort_data: django.db.models.QuerySet
        :return: The average comfort level.
        :rtype: float
        """
        return comfort_data.aggregate(Avg('comfort'))['comfort__avg']

    def _get_comfort_level_distribution(self, comfort_data: Comfort) -> List[
            Dict[str, int]]:
        """
        Get the comfort level distribution.

        :param comfort_data: The comfort data queryset.
        :type comfort_data: django.db.models.QuerySet
        :return: The comfort level distribution.
        :rtype: List[Dict[str, int]]
        """
        comfort_level_distribution = list(
            comfort_data.values('comfort').annotate(
                count=Count('comfort')).order_by('comfort')
        )
        unique_comfort_levels = {}
        for entry in comfort_level_distribution:
            comfort = entry['comfort']
            if comfort not in unique_comfort_levels:
                unique_comfort_levels[comfort] = entry

        return list(unique_comfort_levels.values())

    def _group_data_by_integrate(self, comfort_data: Comfort) -> Dict[
            int, Dict[str, List]]:
        """
        Group the comfort data by integrate.

        :param comfort_data: The comfort data queryset.
        :type comfort_data: django.db.models.QuerySet
        :return: The grouped data by integrate.
        :rtype: Dict[int, Dict[str, List]]
        """
        integrate_data = {}
        for comfort in comfort_data:
            integrate = comfort.integrate
            if integrate not in integrate_data:
                integrate_data[integrate] = {
                    'comfort_levels': [],
                    'upper_labels': [],
                    'lower_labels': [],
                    'temperatures': [],
                    'humidities': []
                }

                predictions = Prediction.objects.filter(
                    integrate=integrate).order_by('timestamp')
                for prediction in predictions:
                    integrate_data[integrate]['upper_labels'].append(
                        prediction.predicted_upper)
                    integrate_data[integrate]['lower_labels'].append(
                        prediction.predicted_lower)

                sensors = Sensor.objects.filter(
                    integrate=integrate).order_by("timestamp")
                for sensor in sensors:
                    if sensor.local_temp:
                        integrate_data[integrate]['temperatures'].append(
                            sensor.local_temp)
                    if sensor.local_humid:
                        integrate_data[integrate]['humidities'].append(
                            sensor.local_humid)

            integrate_data[integrate]['comfort_levels'].append(
                comfort.comfort)

        return integrate_data

    def _get_comfort_level_details(self, integrate_data: Dict[
            int, Dict[str, List]]) -> Dict[int, Dict[str, object]]:
        """
        Get the comfort level details.

        :param integrate_data: The grouped data by integrate.
        :type integrate_data: Dict[int, Dict[str, List]]
        :return: The comfort level details.
        :rtype: Dict[int, Dict[str, object]]
        """
        comfort_level_details = {}
        for data in integrate_data.values():
            comfort_levels = data['comfort_levels']
            upper_labels = data['upper_labels']
            lower_labels = data['lower_labels']
            temperatures = data['temperatures']
            humidities = data['humidities']

            for i, comfort_level in enumerate(comfort_levels):
                upper_label = upper_labels[i] if i < len(
                    upper_labels) else None
                lower_label = lower_labels[i] if i < len(
                    upper_labels) else None

                if comfort_level not in comfort_level_details:
                    comfort_level_details[comfort_level] = {
                        'count': 0,
                        'avg_temp': 0,
                        'avg_humid': 0,
                        'upper_labels': {},
                        'lower_labels': {}
                    }

                comfort_level_details[comfort_level]['count'] += 1
                if temperatures:
                    comfort_level_details[comfort_level]['avg_temp'] += sum(
                        temperatures) / len(temperatures)
                if humidities:
                    comfort_level_details[comfort_level]['avg_humid'] += sum(
                        humidities) / len(humidities)

                if upper_label in comfort_level_details[comfort_level][
                        'upper_labels']:
                    comfort_level_details[comfort_level]['upper_labels'][
                        upper_label] += 1
                else:
                    comfort_level_details[comfort_level]['upper_labels'][
                        upper_label] = 1

                if lower_label in comfort_level_details[comfort_level][
                        'lower_labels']:
                    comfort_level_details[comfort_level]['lower_labels'][
                        lower_label] += 1
                else:
                    comfort_level_details[comfort_level]['lower_labels'][
                        lower_label] = 1

        return comfort_level_details

    def _get_label_counts(self) -> Dict[str, int]:
        """
        Get the clothing label counts.

        :return: The clothing label counts.
        :rtype: Dict[str, int]
        """
        upper_labels = Prediction.objects.values_list('predicted_upper',
                                                      flat=True)
        lower_labels = Prediction.objects.values_list('predicted_lower',
                                                      flat=True)
        all_labels = list(upper_labels) + list(lower_labels)
        label_counts = {}
        for label in all_labels:
            if label in label_counts:
                label_counts[label] += 1
            else:
                label_counts[label] = 1

        return label_counts
