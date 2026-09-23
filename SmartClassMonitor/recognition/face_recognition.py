import cv2
import numpy as np
from insightface.app import FaceAnalysis


class FaceRecognizer:
    def __init__(self):
        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"]
        )

        self.app.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )

        self.known_faces = {}

    def add_face(self, student_id, face_image):
        faces = self.app.get(face_image)

        if not faces:
            return False

        embedding = faces[0].embedding
        embedding = embedding / np.linalg.norm(embedding)

        self.known_faces[student_id] = embedding

        return True

    def recognize(self, face_image, threshold=0.45):
        if not self.known_faces:
            return None

        faces = self.app.get(face_image)

        if not faces:
            return None

        return self.recognize_embedding(
            faces[0].embedding,
            threshold
        )

    def recognize_embedding(self, embedding, threshold=0.45):
        if not self.known_faces:
            return None

        embedding = embedding / np.linalg.norm(embedding)

        best_student = None
        best_score = -1

        for student_id, known_embedding in self.known_faces.items():
            score = float(np.dot(embedding, known_embedding))

            if score > best_score:
                best_score = score
                best_student = student_id

        if best_score < threshold:
            return None

        return best_student