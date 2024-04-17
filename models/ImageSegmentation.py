"""The module containing the image segmentation class."""
import cv2
import numpy as np
import supervision as sv
from segment_anything import sam_model_registry, SamPredictor
from ultralytics import YOLO


class ImageSegmentation:
    """
    The ImageSegmentation class is responsible for segmenting the image.

    The class uses the YOLO model to detect the clothing items in the image.
    The detected clothing items are then segmented using the SAM model.
    """

    def __init__(self):
        """Initialize the ImageSegmentation class."""
        self.model = YOLO("models/weights/best.pt")
        self.pp_model = YOLO("models/weights/yolov9c.pt")
        self.device = "cpu"
        self.checkpoint_path = "models/weights/sam_vit_b_01ec64.pth"
        self.model_type = "vit_b"
        self.sam = sam_model_registry[self.model_type](
            checkpoint=self.checkpoint_path).to(device=self.device)
        self.mask_predictor = SamPredictor(self.sam)
        self.box_annotator = sv.BoundingBoxAnnotator(
            color=sv.Color.YELLOW,
            color_lookup=sv.ColorLookup.INDEX)
        self.mask_annotator = sv.MaskAnnotator(
            color_lookup=sv.ColorLookup.INDEX)
        self.label_annotator = sv.LabelAnnotator(
            text_position=sv.Position.CENTER,
            color_lookup=sv.ColorLookup.INDEX)
        self.corner_annotator = sv.BoxCornerAnnotator(color=sv.Color.GREEN)

    def segment_image(self, image_path: str) -> tuple:
        """
        Segment the image using the YOLO model.

        :param image_path: The path of the image to segment.
        :type image_path: str
        :return: The annotated image and labels.
        :rtype: tuple(numpy.ndarray, list)
        """
        results = self.model(image_path, imgsz=480)
        pp_results = self.pp_model(image_path, imgsz=480)
        annotated_image = None
        all_labels = []

        for i, pr in enumerate(pp_results):
            annotated_image = cv2.imread(image_path)
            self.mask_predictor.set_image(annotated_image)

            pp_detections = sv.Detections.from_ultralytics(pr)
            pp_detections = pp_detections[pp_detections.class_id == 0]
            annotated_image = self.corner_annotator.annotate(annotated_image,
                                                             pp_detections)

            for box in pr.boxes:
                input_box = np.array(box.xyxy.tolist()[0])
                masks, _, _ = self.mask_predictor.predict(
                    point_coords=None,
                    point_labels=None,
                    box=input_box[None, :],
                    multimask_output=False,
                )

                pp_detections = sv.Detections(
                    xyxy=sv.mask_to_xyxy(masks=masks),
                    mask=masks,
                    class_id=np.array(box.cls.tolist()),
                    confidence=np.array(box.conf.tolist())
                ).with_nms(threshold=0.1)
                pp_detections = pp_detections[pp_detections.class_id == 0]
                annotated_image = self.mask_annotator.annotate(
                    scene=annotated_image, detections=pp_detections)

            result = results[i]
            detections = sv.Detections.from_ultralytics(result).with_nms(
                threshold=0.1)

            labels: list = self._extract_labels(result, detections)

            all_labels += [self._determine_type(label) for label in labels]
            annotated_image = self.box_annotator.annotate(
                scene=annotated_image, detections=detections)
            annotated_image = self.label_annotator.annotate(
                scene=annotated_image, detections=detections,
                labels=[str(label) for label in labels])

        return annotated_image, all_labels

    def _extract_labels(self, result,
                        detections: sv.Detections) -> list:
        """
        Extract the labels from the detections.

        :param result: The YOLO result object.
        :type result: YOLO.Results
        :param detections: The detections object.
        :type detections: sv.Detections
        :return: The extracted labels.
        :rtype: list
        """
        labels = [f"{result.names[class_id]}" for
                  xy, mask, confidence, class_id, tracker_id, data in
                  detections]
        return labels

    def _determine_type(self, label: str) -> tuple:
        """
        Determine the type of clothing item based on the label.

        :param label: The label of the clothing item.
        :type label: str
        :return: The upper and lower labels.
        :rtype: tuple
        """
        upper_label, lower_label = None, None
        if label in ['shorts', 'skirt', 'trousers']:
            lower_label = label
        else:
            upper_label = label
        return upper_label, lower_label

    def _save_segmented_image(self, annotated_image: np.ndarray,
                              output_path: str) -> None:
        """
        Save the annotated image to the specified output path.

        :param annotated_image: The annotated image.
        :type annotated_image: numpy.ndarray
        :param output_path: The output path to save the image.
        :type output_path: str
        """
        cv2.imwrite(output_path, annotated_image)
