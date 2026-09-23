from ultralytics import YOLO


class FaceDetector:
    def __init__(self, model_path="yolov12n-face.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(
            frame,
            conf=0.5,
            verbose=False
        )

        result = results[0]

        detections = []

        if result.boxes is None:
            return detections

        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            confidence = float(box.conf[0].item())

            detections.append({
                "bbox": (
                    int(x1),
                    int(y1),
                    int(x2 - x1),
                    int(y2 - y1)
                ),
                "confidence": confidence
            })

        return detections