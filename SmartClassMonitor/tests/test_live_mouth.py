import cv2
import time

from camera.camera_manager import CameraManager
from detection.vision_pipeline import VisionPipeline
from detection.face_detection import FaceDetector
from recognition.face_person_matcher import FacePersonMatcher
from behaviour.mouth_motion import MouthMotionDetector


camera = CameraManager(camera_index=0)
vision = VisionPipeline()
face_detector = FaceDetector()
matcher = FacePersonMatcher()

mouth_detector = MouthMotionDetector(
    opening_threshold=0.40,
    closing_threshold=0.60,
    required_cycles=2
)

camera.start()

print()
print("==============================================")
print(" SmartClassMonitor Live Mouth Calibration")
print("==============================================")
print()
print("Controls:")
print("  Q = Quit")
print()
print("Test naturally:")
print("  1. Stay still")
print("  2. Move your head")
print("  3. Slightly open your mouth")
print("  4. Open your mouth widely")
print("  5. Repeatedly open and close your mouth")
print()

frame_count = 0

try:

    while True:

        frame = camera.camera.read()

        if frame is None:
            print("ERROR: Could not read camera frame.")
            break

        frame_count += 1

        # Person tracking
        output, tracked_people = vision.process(frame)

        # Face detection
        faces = face_detector.detect(frame)

        for face in faces:

            x, y, width, height = face["bbox"]

            face_bbox = (
                x,
                y,
                x + width,
                y + height
            )

            person = matcher.match(
                face_bbox,
                tracked_people
            )

            if person is None:
                continue

            person_id = person["id"]

            result = mouth_detector.detect(
                frame,
                face_bbox,
                person_id
            )

            opening = result["opening"]
            talking = result["talking"]

            # Draw face box
            cv2.rectangle(
                output,
                (x, y),
                (x + width, y + height),
                (255, 255, 255),
                2
            )

            # Display values
            cv2.putText(
                output,
                f"Opening: {opening:.3f}",
                (x, y - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                output,
                f"Talking: {talking}",
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            print(
                f"Opening={opening:.3f} | "
                f"Talking={talking}"
            )

        cv2.imshow(
            "SmartClassMonitor - Mouth Calibration",
            output
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

finally:

    camera.stop()
    cv2.destroyAllWindows()