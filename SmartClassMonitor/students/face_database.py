class FaceDatabase:
    def __init__(self):
        self.faces = {}

    def add_face(self, student_id, face_data):
        self.faces[student_id] = face_data

    def get_face(self, student_id):
        return self.faces.get(student_id)

    def get_all_faces(self):
        return self.faces

    def remove_face(self, student_id):
        if student_id in self.faces:
            del self.faces[student_id]

    def clear(self):
        self.faces.clear()