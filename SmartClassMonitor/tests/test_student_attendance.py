import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from students.student_database import StudentDatabase
from database.database import Database
from attendance.register import AttendanceRegister
from attendance.student_attendance import StudentAttendance


student_database = StudentDatabase()

student_database.add_student(
    "student_001",
    "Student 1"
)

student_database.add_student(
    "student_002",
    "Student 2"
)

student_database.add_student(
    "student_003",
    "Student 3"
)

database = Database("database/classroom.db")
database.initialize()

attendance_register = AttendanceRegister(database)

student_attendance = StudentAttendance(
    student_database,
    attendance_register
)

test_date = "2026-09-22"

print()
print("==============================================")
print(" SmartClassMonitor Student Attendance Test")
print("==============================================")
print()

print("Complete attendance register:")

register = student_attendance.get_daily_register(
    test_date
)

for student in register:
    print(
        f"{student['student_id']} | "
        f"{student['name']} | "
        f"{student['status']} | "
        f"{student['timestamp']}"
    )

print()

print(
    f"Present count: "
    f"{student_attendance.get_present_count(test_date)}"
)

print(
    f"Absent count: "
    f"{student_attendance.get_absent_count(test_date)}"
)

print(
    f"Late count: "
    f"{student_attendance.get_late_count(test_date)}"
)

database.close()

print()
print("Student Attendance test PASSED.")