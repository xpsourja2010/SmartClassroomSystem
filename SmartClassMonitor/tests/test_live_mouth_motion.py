import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import cv2

from camera.droidcam import DroidCam
from detection.face_detection import FaceDetector
from behaviour.mouth_motion import MouthMotionDetector


camera = DroidCam()
face_detector = FaceDetector()

mouth_detector = MouthMotionDetector(
    movement_threshold=0.08,
    required_cycles=2
)

camera.open()

print()
print("==============================================")
print(" SmartClassMonitor Live Mouth Cycle Test")
print("==============================================")
print()
print("1. Keep mouth still.")
print("2. Slowly move your head.")
print("3. Turn your head repeatedly.")
print("4. Open and close your mouth repeatedly.")
print()
print("Press Q to stop.")
print()

talking_frames = 0
max_opening = 0.0

try:
    while True:

        frame = camera.read()

        if frame is None:
            print("ERROR: Could not read camera frame.")
            break

        faces = face_detector.detect(frame)

        for index, face in enumerate(faces):

            x, y, w, h = face["bbox"]

            face_bbox = (
                x,
                y,
                x + w,
                y + h
            )

            result = mouth_detector.detect(
                frame,
                face_bbox,
                index
            )

            opening = result["opening"]
            talking = result["talking"]
            cycle = result["cycle"]

            max_opening = max(
                max_opening,
                opening
            )

            if talking:
                talking_frames += 1

            if talking:
                status = "POSSIBLE TALKING"
            elif cycle:
                status = "MOUTH CYCLE"
            else:
                status = "NORMAL"

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"{status}  Open:{opening:.3f}",
                (x, max(y - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )

        cv2.imshow(
            "SmartClassMonitor - Live Mouth Cycle",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    camera.release()
    cv2.destroyAllWindows()

print()
print("Maximum opening:", round(max_opening, 3))
print("Talking frames:", talking_frames)
print("Live Mouth Cycle test complete.")