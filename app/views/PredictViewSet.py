"""The module defines the PredictViewSet class."""
import os
import imghdr

import cv2
import numpy as np
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response

from app.models import Integrate, Prediction, Image, Sensor
from app.serializers import PredictionSerializer, ImageSerializer, \
    SensorSerializer, ComfortSerializer
from models import ImageSegmentation, ComfortClassifier


class PredictViewSet(viewsets.ViewSet):
    """ViewSet for handling Prediction-related operations."""

    parser_classes = (MultiPartParser, FormParser)

    def create(self, request) -> Response:
        """
        Create a new Prediction object for a specific integrate.

        :param request: The HTTP request with prediction data.
        :type request: rest_framework.request.Request
        :return: Response with created prediction or error.
        :rtype: rest_framework.response.Response
        """
        secret = request.data.get('secret')
        image_file = request.data.get('image')

        if secret and self._isvalid(image_file):
            integrate = self._get_or_create_integrate(secret)
            image_path = self._save_image(image_file)
            annotated_image, labels = self._segment_image(image_path)
            self._save_predictions(labels, integrate)
            self._save_annotated_image(annotated_image, request, integrate)
            response_data = self._get_response_data(integrate, request)

            local_temp, local_humid = self._get_sensor_data(integrate)
            if local_temp and local_humid:
                comfort_levels = self._predict_comfort_level(labels,
                                                             local_temp,
                                                             local_humid,
                                                             integrate)
                response_data['comfort_level'] = comfort_levels

            self._delete_excess_images('uploads')
            self._delete_excess_images('detected_images')

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Missing required data'},
                        status=status.HTTP_400_BAD_REQUEST)

    def _get_or_create_integrate(self, secret: str) -> Integrate:
        """
        Get or create an Integration object based on the secret.

        :param secret: The secret key for the integrate.
        :type secret: str
        :return: The Integration object.
        :rtype: app.models.Integrate
        """
        integrate = Integrate.objects.filter(secret=secret).first()
        if not integrate:
            integrate = Integrate.objects.create(secret=secret)
        return integrate

    def _save_image(self, image_file: ContentFile) -> str:
        """
        Save the uploaded image file.

        :param image_file: The uploaded image file.
        :type image_file: django.core.files.uploadedfile.InMemoryUploadedFile
        :return: The path of the saved image.
        :rtype: str
        """
        image_path = default_storage.save('uploads/' + image_file.name,
                                          ContentFile(image_file.read()))
        return "media/" + image_path

    def _segment_image(self, image_path: str) -> tuple:
        """
        Segment the image using the ImageSegmentation model.

        :param image_path: The path of the image to segment.
        :type image_path: str
        :return: The annotated image and labels.
        :rtype: tuple(numpy.ndarray, list)
        """
        segmentation = ImageSegmentation()
        annotated_image, labels = segmentation.segment_image(image_path)
        return annotated_image, labels

    def _save_predictions(self, labels: list,
                          integrate: Integrate) -> None:
        """
        Save the predicted labels.

        :param labels: The predicted labels.
        :type labels: list
        :param integrate: The Integration object.
        :type integrate: app.models.Integrate
        """
        for upper, lower in labels:
            prediction_serializer = PredictionSerializer(
                data={'predicted_upper': upper, 'predicted_lower': lower})
            if prediction_serializer.is_valid():
                prediction_serializer.save(integrate=integrate)

    def _save_annotated_image(self, annotated_image: np.ndarray,
                              request: Request,
                              integrate: Integrate) -> None:
        """
        Save the annotated image.

        :param annotated_image: The annotated image.
        :type annotated_image: numpy.ndarray
        :param request: The HTTP request.
        :type request: rest_framework.request.Request
        :param integrate: The Integration object.
        :type integrate: app.models.Integrate
        """
        _, frame = cv2.imencode('.png', annotated_image)
        img_file = ContentFile(frame.tobytes())
        img_file.name = 'segmented_image.jpg'
        image_serializer = ImageSerializer(data={'detected_image': img_file},
                                           context={'request': request})
        if image_serializer.is_valid():
            image_serializer.save(integrate=integrate)
        else:
            raise Exception(image_serializer.errors)

    def _delete_excess_images(self, folder: str) -> None:
        """
        Delete excess images from the specified folder.

        :param folder: The folder name.
        :type folder: str
        """
        media_folder = os.path.join(settings.MEDIA_ROOT, folder)
        images = list(os.listdir(media_folder))
        if len(images) > 10:
            images_to_delete = images[:5]
            for image in images_to_delete:
                image_path = os.path.join(media_folder, image)
                os.remove(image_path)

    def _predict_comfort_level(self, labels: list,
                               local_temp: float,
                               local_humid: float,
                               integrate: Integrate) -> list:
        """
        Predict the comfort level based on labels, temperature, and humidity.

        :param labels: The predicted labels.
        :type labels: list
        :param local_temp: The local temperature.
        :type local_temp: float
        :param local_humid: The local humidity.
        :type local_humid: float
        :param integrate: The Integration object.
        :type integrate: app.models.Integrate
        :return: The predicted comfort levels.
        :rtype: list
        """
        comfort_classifier = ComfortClassifier()
        comfort_levels = comfort_classifier.predict_comfort_level(labels,
                                                                  local_temp,
                                                                  local_humid)
        comfort_data = []
        for comfort in comfort_levels:
            comfort_serializer = ComfortSerializer(data={'comfort': comfort})
            if comfort_serializer.is_valid():
                comfort_data.append(comfort_serializer.data['comfort'])
            else:
                raise Exception(comfort_serializer.errors)
        return comfort_data

    def _get_response_data(self, integrate: Integrate,
                           request: Request) -> dict:
        """
        Get the response data for the given integrate.

        :param integrate: The Integration object.
        :type integrate: app.models.Integrate
        :param request: The HTTP request.
        :type request: rest_framework.request.Request
        :return: The response data.
        :rtype: dict
        """
        predictions = Prediction.objects.filter(integrate=integrate)
        images = Image.objects.filter(integrate=integrate)
        sensors = Sensor.objects.filter(integrate=integrate)

        response_data = {
            'predictions': PredictionSerializer(predictions, many=True).data,
            'images': ImageSerializer(images, many=True,
                                      context={'request': request}).data,
            'sensors': SensorSerializer(sensors, many=True).data,
        }
        return response_data

    def _get_sensor_data(self, integrate: Integrate) -> tuple:
        """
        Get the sensor data for the given integrate.

        :param integrate: The Integration object.
        :type integrate: app.models.Integrate
        :return: The local temperature and humidity.
        :rtype: tuple(float, float)
        """
        sensor_data = Sensor.objects.filter(integrate=integrate).first()
        if not sensor_data:
            return None, None
        return sensor_data.local_temp, sensor_data.local_humid

    def _isvalid(self, file: ContentFile) -> bool:
        """
        Check if the given file is a valid image file.

        :param file: The file to be validated.
        :type file: django.core.files.uploadedfile.InMemoryUploadedFile
        :return: True if the file is a valid image, False otherwise.
        :rtype: bool
        """
        valid_extensions = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'webp']
        if not file:
            return False
        image_type = imghdr.what(file)
        return image_type in valid_extensions
