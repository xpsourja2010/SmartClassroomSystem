import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

import cv2

from recognition.recognition_manager import RecognitionManager
from attendance.attendance import AttendanceManager


# --------------------------------------------------
# INITIALIZE
# --------------------------------------------------

recognition = RecognitionManager()
attendance = AttendanceManager()


# --------------------------------------------------
# LOAD TEST FACE
# --------------------------------------------------

face_1 = cv2.imread(
    "tests/test_face_1.jpg"
)

if face_1 is None:
    print("ERROR: test_face_1.jpg not found.")
    sys.exit()


# --------------------------------------------------
# REGISTER STUDENT
# --------------------------------------------------

if not recognition.register_face(
    "student_001",
    face_1
):
    print("ERROR: Could not register student.")
    sys.exit()


print("Student registered.")


# --------------------------------------------------
# RECOGNIZE STUDENT
# --------------------------------------------------

student_id = recognition.recognize_face(
    face_1
)

print("Recognized student:", student_id)


# --------------------------------------------------
# MARK ATTENDANCE
# --------------------------------------------------

if student_id is not None:

    record = attendance.mark_present(
        student_id,
        "Student 1"
    )

    print("\nAttendance record:")
    print(record)


# --------------------------------------------------
# VERIFY
# --------------------------------------------------

saved_record = attendance.get_attendance(
    "student_001"
)

if (
    student_id == "student_001"
    and saved_record is not None
    and saved_record["status"] == "PRESENT"
):
    print("\nIdentity → Attendance test PASSED.")
else:
    print("\nIdentity → Attendance test FAILED.")