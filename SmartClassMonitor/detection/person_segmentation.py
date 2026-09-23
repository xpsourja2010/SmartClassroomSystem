from ultralytics import YOLO


class PersonSegmenter:
    def __init__(self, model_path="yolo26n-seg.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(
            frame,
            classes=[0],
            conf=0.4,
            verbose=False
        )

        return results[0]