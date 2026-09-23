import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from behaviour.talking import TalkingDetector


detector = TalkingDetector(
    movement_threshold=2.5,
    required_movement_frames=3
)

print()
print("==============================================")
print(" SmartClassMonitor Talking Detector Test")
print("==============================================")
print()

print("Testing stationary mouth:")

for frame in range(5):
    result = detector.detect(
        "student_001",
        [(100, 100)]
    )

    print(
        f"Frame {frame + 1}: "
        f"Talking = {result}"
    )

print()

detector.reset("student_001")

print("Testing repeated mouth movement:")

test_positions = [
    (100, 100),
    (105, 100),
    (110, 100),
    (115, 100),
    (120, 100)
]

for frame, position in enumerate(test_positions):
    result = detector.detect(
        "student_001",
        [position]
    )

    print(
        f"Frame {frame + 1}: "
        f"Mouth = {position} | "
        f"Talking = {result}"
    )

print()

if detector.get_state("student_001"):
    print("Movement-based talking detection triggered.")
else:
    print("Talking detection did not trigger.")

print()
print("Talking Detector test PASSED.")