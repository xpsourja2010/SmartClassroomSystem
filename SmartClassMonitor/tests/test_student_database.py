import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from students.student_database import StudentDatabase


db = StudentDatabase()

# Add students
db.add_student("student_001", "Student 1")
db.add_student("student_002", "Student 2")
db.add_student("student_003", "Student 3")

print("All students:")
print(db.get_all_students())

print("\nGet student_002:")
print(db.get_student("student_002"))

# Remove one student
db.remove_student("student_003")

print("\nAfter removing student_003:")
print(db.get_all_students())