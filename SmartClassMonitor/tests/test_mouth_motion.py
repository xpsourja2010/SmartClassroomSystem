import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np

from behaviour.mouth_motion import MouthMotionDetector


# Create detector
detector = MouthMotionDetector(
    opening_threshold=0.40,
    closing_threshold=0.60,
    required_cycles=2
)


# Create base frame
frame_1 = np.zeros(
    (480, 640, 3),
    dtype=np.uint8
)


# Face bounding box
face_bbox = (200, 100, 400, 300)


print()
print("==============================================")
print(" SmartClassMonitor Mouth Cycle Test")
print("==============================================")
print()


# ------------------------------------------------
# TEST 1: IDENTICAL FRAMES
# ------------------------------------------------

print("Testing identical frames:")

result = detector.detect(
    frame_1,
    face_bbox,
    "student_001"
)

result = detector.detect(
    frame_1,
    face_bbox,
    "student_001"
)

print(f"Opening: {result['opening']:.3f}")
print(f"Talking: {result['talking']}")

print()


# ------------------------------------------------
# RESET
# ------------------------------------------------

detector.reset("student_001")


# ------------------------------------------------
# TEST 2: REPEATED OPEN/CLOSE CYCLES
# ------------------------------------------------

print("Testing repeated open/close cycles:")


# Closed mouth
closed_frame = frame_1.copy()


# Simulated open mouth
open_frame = frame_1.copy()

cv2.rectangle(
    open_frame,
    (250, 200),
    (350, 270),
    (255, 255, 255),
    -1
)


# Open → close → open → close...
frames = [
    closed_frame,
    open_frame,
    closed_frame,
    open_frame,
    closed_frame,
    open_frame
]


for number, frame in enumerate(frames, start=1):

    result = detector.detect(
        frame,
        face_bbox,
        "student_001"
    )

    print(
        f"Frame {number}: "
        f"Opening={result['opening']:.3f} | "
        f"Cycle={result['cycle']} | "
        f"Talking={result['talking']}"
    )


print()


# ------------------------------------------------
# FINAL RESULT
# ------------------------------------------------

if result["talking"]:
    print("Repeated mouth cycles detected.")
else:
    print("Repeated mouth cycles NOT detected.")


print()
print("Mouth Cycle test complete.")