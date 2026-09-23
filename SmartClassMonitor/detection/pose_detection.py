from ultralytics import YOLO


class PoseDetector:
    def __init__(self, model_path="yolo26n-pose.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(
            frame,
            classes=[0],
            conf=0.4,
            verbose=False
        )

        return results[0]