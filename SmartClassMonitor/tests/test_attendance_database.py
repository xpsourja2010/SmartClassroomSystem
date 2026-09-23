import sys
from pathlib import Path

# Allow imports from project root
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from attendance.attendance import AttendanceManager
from database.database import Database
from datetime import datetime


# ============================================================
# TEST DATABASE
# ============================================================

db = Database("database/test_attendance.db")

db.initialize()


# ============================================================
# ATTENDANCE MANAGER CONNECTED TO DATABASE
# ============================================================

attendance = AttendanceManager(
    database=db
)


# ============================================================
# TEST ATTENDANCE
# ============================================================

test_time = datetime(
    2026,
    9,
    22,
    18,
    0,
    0
)

print("Marking student present...")

record = attendance.mark_present(
    "student_001",
    "Student 1",
    test_time
)

print("In-memory record:")
print(record)


# ============================================================
# READ FROM DATABASE
# ============================================================

print()
print("Reading from SQLite database...")

database_records = db.get_all_attendance()

for record in database_records:
    print(record)


# ============================================================
# CLOSE
# ============================================================

db.close()


print()
print("Attendance → SQLite integration PASSED.")