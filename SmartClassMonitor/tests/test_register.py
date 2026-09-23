import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from database.database import Database
from attendance.register import AttendanceRegister


database = Database("database/classroom.db")
database.initialize()

register = AttendanceRegister(database)

test_date = "2026-09-22"

print()
print("==============================================")
print(" SmartClassMonitor Attendance Register Test")
print("==============================================")
print()

print("Daily attendance:")
records = register.get_daily_attendance(test_date)

for record in records:
    print(
        f"{record[0]} | "
        f"{record[1]} | "
        f"{record[2]} | "
        f"{record[3]}"
    )

print()

print("Present students:")
present_students = register.get_present_students(test_date)

for student in present_students:
    print(f"{student[0]} - {student[1]}")

print()

print("Late students:")
late_students = register.get_late_students(test_date)

for student in late_students:
    print(f"{student[0]} - {student[1]}")

print()

print("Checking student_002:")
student = register.get_student_attendance(
    "student_002",
    test_date
)

print(student)

print()

if register.is_student_present(
    "student_002",
    test_date
):
    print("student_002 is PRESENT.")
else:
    print("student_002 is NOT PRESENT.")

database.close()

print()
print("Attendance Register test PASSED.")