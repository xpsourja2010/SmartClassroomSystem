import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from datetime import datetime, timedelta

from attendance.attendance import AttendanceManager
from attendance.late_detection import LateDetector


# --------------------------------------------------
# ATTENDANCE TEST
# --------------------------------------------------

attendance = AttendanceManager(
    late_after_minutes=5
)

test_time = datetime(
    2026,
    9,
    22,
    8,
    5,
    0
)

record = attendance.mark_present(
    "student_001",
    "Student 1",
    test_time
)

print("Attendance record:")
print(record)

if (
    record["student_id"] == "student_001"
    and record["status"] == "PRESENT"
):
    print("Present test PASSED.")
else:
    print("Present test FAILED.")


# --------------------------------------------------
# DUPLICATE TEST
# --------------------------------------------------

attendance.mark_present(
    "student_001",
    "Student 1",
    test_time + timedelta(minutes=2)
)

records = attendance.get_all_attendance()

print("\nRecords after duplicate detection:")
print(records)

if len(records) == 1:
    print("Duplicate prevention test PASSED.")
else:
    print("Duplicate prevention test FAILED.")


# --------------------------------------------------
# LATE DETECTION TEST
# --------------------------------------------------

late_detector = LateDetector(
    late_after_minutes=5
)

class_start = datetime(
    2026,
    9,
    22,
    8,
    0,
    0
)

on_time = datetime(
    2026,
    9,
    22,
    8,
    4,
    0
)

late_time = datetime(
    2026,
    9,
    22,
    8,
    6,
    0
)

print("\nTesting late detection...")

print(
    "At 08:04:",
    late_detector.is_late(
        class_start,
        on_time
    )
)

print(
    "At 08:06:",
    late_detector.is_late(
        class_start,
        late_time
    )
)

if (
    late_detector.is_late(class_start, on_time) is False
    and late_detector.is_late(class_start, late_time) is True
):
    print("Late detection test PASSED.")
else:
    print("Late detection test FAILED.")