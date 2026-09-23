class StudentDatabase:
    def __init__(self):
        self.students = {}

    def add_student(self, student_id, name):
        self.students[student_id] = {
            "student_id": student_id,
            "name": name
        }

    def get_student(self, student_id):
        return self.students.get(student_id)

    def get_all_students(self):
        return list(self.students.values())

    def remove_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]

    def clear(self):
        self.students.clear()