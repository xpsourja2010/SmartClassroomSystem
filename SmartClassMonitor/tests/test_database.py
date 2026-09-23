import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.database import Database
from datetime import datetime


db = Database("database/test_classroom.db")

db.initialize()

test_time = datetime(2026, 9, 22, 10, 0, 0)

print("Adding attendance...")

added = db.add_attendance(
    "student_001",
    "Student 1",
    "PRESENT",
    test_time
)

print("First insert:", added)

duplicate = db.add_attendance(
    "student_001",
    "Student 1",
    "PRESENT",
    test_time
)

print("Duplicate insert:", duplicate)

print("\nAttendance records:")

records = db.get_all_attendance()

for record in records:
    print(record)

db.close()

print("\nDatabase test PASSED.")