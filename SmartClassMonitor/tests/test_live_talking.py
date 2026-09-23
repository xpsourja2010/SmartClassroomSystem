import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import cv2

from camera.droidcam import DroidCam
from detection.pose_detection import PoseDetector
from behaviour.talking import TalkingDetector


camera = DroidCam()
pose_detector = PoseDetector()
talking_detector = TalkingDetector(
    movement_threshold=2.5,
    required_movement_frames=3
)

camera.open()

print()
print("==============================================")
print(" SmartClassMonitor Live Talking Test")
print("==============================================")
print()
print("YOLO Pose + Talking Detector enabled.")
print("Press Q to stop.")
print()

try:
    while True:
        frame = camera.read()

        if frame is None:
            print("ERROR: Could not read camera frame.")
            break

        pose_result = pose_detector.detect(frame)

        output = pose_result.plot(
            boxes=True
        )

        if pose_result.keypoints is not None:
            keypoints_data = pose_result.keypoints.xy.cpu().numpy()

            for person_index, person_keypoints in enumerate(
                keypoints_data
            ):
                if len(person_keypoints) == 0:
                    continue

                person_id = person_index

                # YOLO pose uses facial keypoints near the top
                # of the keypoint array.
                #
                # For this first live test we use the
                # nose keypoint as a stable facial reference.
                nose = person_keypoints[0]

                if nose[0] == 0 and nose[1] == 0:
                    continue

                talking = talking_detector.detect(
                    person_id,
                    [tuple(nose)]
                )

                label = (
                    f"Person {person_id}: "
                    f"{'POSSIBLE TALKING' if talking else 'NOT TALKING'}"
                )

                x = max(int(nose[0]) - 80, 10)
                y = max(int(nose[1]) - 20, 30)

                cv2.rectangle(
                    output,
                    (x, y - 30),
                    (x + 300, y + 5),
                    (0, 0, 0),
                    -1
                )

                cv2.putText(
                    output,
                    label,
                    (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA
                )

        cv2.imshow(
            "SmartClassMonitor - Live Talking Test",
            output
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    camera.release()
    cv2.destroyAllWindows()

print()
print("Live Talking test complete.")