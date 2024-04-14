from rest_framework import status, viewsets
from rest_framework.response import Response
from app.serializers import PredictionSerializer, ImageSerializer
from app.models import Integration, Prediction, Image
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from models import ImageSegmentation
import cv2


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
            integration = Integration.objects.create(secret=secret)
            image_path = default_storage.save('uploads/' + image_file.name,
                                              ContentFile(image_file.read()))
            image_path = "media/" + image_path

            segmentation = ImageSegmentation()
            annotated_image, labels = segmentation.segment_image(image_path)

            prediction_serializer = PredictionSerializer(data={'predicted_type': labels[0]})
            if prediction_serializer.is_valid():
                prediction_serializer.save(integration=integration)
            else:
                return Response(prediction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            _, frame = cv2.imencode('.png', annotated_image)
            img_file = ContentFile(frame.tobytes())

            img_file.name = 'segmented_image.jpg'

            image_serializer = ImageSerializer(
                data={'detected_image': img_file},
                context={'request': request})
            if image_serializer.is_valid():
                image = image_serializer.save(integration=integration)
            else:
                return Response(image_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

            default_storage.delete(image_path)

            predictions = Prediction.objects.filter(integration=integration)
            images = Image.objects.filter(integration=integration)

            response_data = {
                'predictions': PredictionSerializer(predictions,
                                                    many=True).data,
                'images': ImageSerializer(images, many=True,
                                          context={'request': request}).data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Missing secret code or image'}, status=status.HTTP_400_BAD_REQUEST)
