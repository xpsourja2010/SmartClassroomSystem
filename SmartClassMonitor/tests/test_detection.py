import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from camera.droidcam import DroidCam
from detection.vision_pipeline import VisionPipeline


camera = DroidCam()
vision = VisionPipeline()

camera.open()

print("SmartClassMonitor vision pipeline started.")
print("Segmentation + Pose + Tracking enabled.")
print("Press Q to stop.")

while True:
    frame = camera.read()

    if frame is None:
        print("ERROR: Could not read camera frame.")
        break

    output, tracked_people = vision.process(frame)

    for person in tracked_people:
        person_id = person["track_id"]
        x1, y1, x2, y2 = map(int, person["bbox"])

        label = f"ID: {person_id}"

        cv2.putText(
            output,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    cv2.imshow(
        "SmartClassMonitor - Vision Pipeline",
        output
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()