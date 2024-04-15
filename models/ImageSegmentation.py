from ultralytics import YOLO
import supervision as sv
from segment_anything import sam_model_registry, SamPredictor
import cv2
import numpy as np


class ImageSegmentation:
    """"""
    def __init__(self):
        self.model = YOLO("models/weights/best.pt")
        self.pp_model = YOLO("models/weights/yolov9c.pt")
        self.device = "cpu"
        self.checkpoint_path = "models/weights/sam_vit_b_01ec64.pth"
        self.model_type = "vit_b"
        self.sam = sam_model_registry[self.model_type](
            checkpoint=self.checkpoint_path).to(device=self.device)
        self.mask_predictor = SamPredictor(self.sam)
        self.box_annotator = sv.BoundingBoxAnnotator(color=sv.Color.YELLOW,
                                                     color_lookup=sv.ColorLookup.INDEX)
        self.mask_annotator = sv.MaskAnnotator(
            color_lookup=sv.ColorLookup.INDEX)
        self.label_annotator = sv.LabelAnnotator(
            text_position=sv.Position.CENTER,
            color_lookup=sv.ColorLookup.INDEX)
        self.corner_annotator = sv.BoxCornerAnnotator(color=sv.Color.GREEN)

    def segment_image(self, image_path):
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
            detections = sv.Detections.from_ultralytics(result).with_nms(threshold=0.1)

            labels = [f"{result.names[class_id]}" for
                      xy, mask, confidence, class_id, tracker_id, data in
                      detections]
            upper_label, lower_label = None, None
            for label in labels:
                if label in ['shorts', 'skirt', 'trousers']:
                    lower_label = label
                else:
                    upper_label = label
                all_labels.append((upper_label, lower_label))

            annotated_image = self.box_annotator.annotate(
                scene=annotated_image, detections=detections)
            annotated_image = self.label_annotator.annotate(
                scene=annotated_image, detections=detections,
                labels=[str(label) for label in labels])

        print("####################################")
        print(f"All labels: {all_labels}")
        return annotated_image, all_labels

    @staticmethod
    def save_segmented_image(annotated_image, output_path):
        """Save an annotated image in local."""
        cv2.imwrite(output_path, annotated_image)
