import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from students.enrollment import Enrollment


enrollment = Enrollment()

# Enroll a student
enrollment.enroll_student(
    "student_001",
    "Student 1",
    "face_data_001"
)

print("Student:")
print(enrollment.get_student("student_001"))

print("\nFace data:")
print(enrollment.get_face("student_001"))