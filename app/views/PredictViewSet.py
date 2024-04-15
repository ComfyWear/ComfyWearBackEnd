import cv2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from app.models import Integration, Prediction, Image, Sensor, Comfort
from app.serializers import PredictionSerializer, ImageSerializer, \
    SensorSerializer, ComfortSerializer
from models import ImageSegmentation, ComfortClassifier


class PredictViewSet(viewsets.ViewSet):
    """ViewSet for handling Prediction-related operations."""
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request):
        """
        Create a new Prediction object for a specific integration.

        :param request: The HTTP request with prediction data.
        :return: Response with created prediction or error.
        """
        secret = request.data.get('secret')
        image_file = request.data.get('image')

        if secret and image_file:
            integration = Integration.objects.filter(secret=secret).first()

            if not integration:
                integration = Integration.objects.create(secret=secret)

            image_path = self.save_image(image_file)
            segmentation = ImageSegmentation()
            annotated_image, labels = segmentation.segment_image(image_path)
            self.save_predictions(labels, integration)
            self.save_annotated_image(annotated_image, request, integration)
            response_data = self.get_response_data(integration, request)

            local_temp, local_humid = self.get_sensor_data(integration)
            if local_temp and local_humid:
                comfort_level = self.predict_comfort_level(labels, local_temp,
                                                           local_humid,
                                                           integration)
                response_data['comfort_level'] = comfort_level

            default_storage.delete(image_path)

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Missing required data'},
                            status=status.HTTP_400_BAD_REQUEST)

    def save_image(self, image_file):
        image_path = default_storage.save('uploads/' + image_file.name,
                                          ContentFile(image_file.read()))
        return "media/" + image_path

    def save_predictions(self, labels, integration):
        for upper, lower in labels:
            prediction_serializer = PredictionSerializer(
                data={'predicted_upper': upper, 'predicted_lower': lower})
            if prediction_serializer.is_valid():
                prediction_serializer.save(integration=integration)

    def save_annotated_image(self, annotated_image, request, integration):
        _, frame = cv2.imencode('.png', annotated_image)
        img_file = ContentFile(frame.tobytes())
        img_file.name = 'segmented_image.jpg'
        image_serializer = ImageSerializer(data={'detected_image': img_file},
                                           context={'request': request})
        if image_serializer.is_valid():
            image = image_serializer.save(integration=integration)
            return image_serializer.data['detected_image']
        else:
            raise Exception(image_serializer.errors)

    def create_sensor_data(self, local_temp, local_humid, integration):
        sensor_serializer = SensorSerializer(
            data={'local_temp': local_temp, 'local_humid': local_humid})
        if sensor_serializer.is_valid():
            sensor_serializer.save(integration=integration)
        else:
            raise Exception(sensor_serializer.errors)

    def predict_comfort_level(self, labels, local_temp, local_humid,
                              integration):
        comfort_classifier = ComfortClassifier()
        comfort_levels = comfort_classifier.predict_comfort_level(labels, local_temp, local_humid)
        for comfort in comfort_levels:
            comfort_serializer = ComfortSerializer(data={'comfort': comfort})
            if comfort_serializer.is_valid():
                comfort_serializer.save(integration=integration)
                return comfort_serializer.data['comfort']
            else:
                raise Exception(comfort_serializer.errors)

    def get_response_data(self, integration, request):
        predictions = Prediction.objects.filter(integration=integration)
        images = Image.objects.filter(integration=integration)
        sensors = Sensor.objects.filter(integration=integration)

        response_data = {
            'predictions': PredictionSerializer(predictions, many=True).data,
            'images': ImageSerializer(images, many=True,
                                      context={'request': request}).data,
            'sensors': SensorSerializer(sensors, many=True).data,
        }
        return response_data

    def get_sensor_data(self, integration: Integration):
        sensor_data = Sensor.objects.filter(integration=integration).first()
        if not sensor_data:
            return None, None
        return sensor_data.local_temp, sensor_data.local_humid
