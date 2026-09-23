from recognition.face_recognition import FaceRecognizer


class RecognitionManager:
    def __init__(self):
        self.recognizer = FaceRecognizer()
        self.identity_map = {}

    def register_face(self, student_id, face_image):
        return self.recognizer.add_face(student_id, face_image)

    def recognize_face(self, face_image, threshold=0.45):
        return self.recognizer.recognize(
            face_image,
            threshold=threshold
        )

    def assign_identity(self, tracking_id, student_id):
        self.identity_map[tracking_id] = student_id

    def get_identity(self, tracking_id):
        return self.identity_map.get(tracking_id)

    def remove_identity(self, tracking_id):
        if tracking_id in self.identity_map:
            del self.identity_map[tracking_id]

    def clear(self):
        self.identity_map.clear()