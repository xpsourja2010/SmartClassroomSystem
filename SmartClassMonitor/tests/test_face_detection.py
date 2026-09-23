import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from camera.droidcam import DroidCam
from detection.face_detection import FaceDetector


camera = DroidCam()
face_detector = FaceDetector()

camera.open()

print("Face detection started.")
print("Press Q to stop.")

while True:
    frame = camera.read()

    if frame is None:
        print("ERROR: Could not read camera frame.")
        break

    faces = face_detector.detect(frame)

    for face in faces:
        x, y, width, height = face["bbox"]

        cv2.rectangle(
            frame,
            (x, y),
            (x + width, y + height),
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "SmartClassMonitor - Face Detection",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()