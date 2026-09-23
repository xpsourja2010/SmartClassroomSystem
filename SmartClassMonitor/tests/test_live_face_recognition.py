import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from camera.droidcam import DroidCam
from recognition.face_recognition import FaceRecognizer


camera = DroidCam()
recognizer = FaceRecognizer()

# Load registered student photos
face_1 = cv2.imread("tests/test_face_1.jpg")
face_2 = cv2.imread("tests/test_face_2.jpg")

if face_1 is None or face_2 is None:
    print("ERROR: Test face images not found.")
    sys.exit()

# Register students
if not recognizer.add_face("student_001", face_1):
    print("ERROR: Could not register student_001.")
    sys.exit()

if not recognizer.add_face("student_002", face_2):
    print("ERROR: Could not register student_002.")
    sys.exit()

print("Face recognition database loaded.")
print("Starting live camera...")
print("Press Q to stop.")

camera.open()

while True:
    frame = camera.read()

    if frame is None:
        print("ERROR: Could not read camera frame.")
        break

    faces = recognizer.app.get(frame)

    for face in faces:
        x1, y1, x2, y2 = map(int, face.bbox)

        embedding = face.embedding
        embedding = embedding / (embedding @ embedding) ** 0.5

        best_student = None
        best_score = -1

        for student_id, known_embedding in recognizer.known_faces.items():
            score = float(embedding @ known_embedding)

            if score > best_score:
                best_score = score
                best_student = student_id

        if best_score >= 0.45:
            label = f"{best_student} ({best_score:.2f})"
        else:
            label = f"Unknown ({best_score:.2f})"

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "SmartClassMonitor - Live Face Recognition",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()