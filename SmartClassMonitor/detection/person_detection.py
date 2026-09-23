import cv2


class PersonDetector:
    def __init__(self):
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=50,
            detectShadows=True
        )

    def detect(self, frame):
        mask = self.background_subtractor.apply(frame)

        _, threshold = cv2.threshold(
            mask,
            200,
            255,
            cv2.THRESH_BINARY
        )

        contours, _ = cv2.findContours(
            threshold,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        detections = []

        for contour in contours:
            area = cv2.contourArea(contour)

            if area < 1500:
                continue

            x, y, width, height = cv2.boundingRect(contour)

            detections.append({
                "bbox": (x, y, width, height),
                "area": area
            })

        return detections