from students.student_database import StudentDatabase
from students.face_database import FaceDatabase


class Enrollment:
    def __init__(self):
        self.student_database = StudentDatabase()
        self.face_database = FaceDatabase()

    def enroll_student(self, student_id, name, face_data):
        self.student_database.add_student(
            student_id,
            name
        )

        self.face_database.add_face(
            student_id,
            face_data
        )

    def get_student(self, student_id):
        return self.student_database.get_student(student_id)

    def get_face(self, student_id):
        return self.face_database.get_face(student_id)