import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
from recognition.face_recognition import FaceRecognizer


recognizer = FaceRecognizer()

face_1 = cv2.imread("tests/test_face_1.jpg")
face_2 = cv2.imread("tests/test_face_2.jpg")

if face_1 is None or face_2 is None:
    print("ERROR: Test face images not found.")
    sys.exit()

print("Adding face 1...")
if recognizer.add_face("student_001", face_1):
    print("Face 1 added successfully.")
else:
    print("ERROR: No face detected in face 1.")

print("Adding face 2...")
if recognizer.add_face("student_002", face_2):
    print("Face 2 added successfully.")
else:
    print("ERROR: No face detected in face 2.")

print("\nTesting face 1...")
result_1 = recognizer.recognize(face_1)
print("Result:", result_1)

print("\nTesting face 2...")
result_2 = recognizer.recognize(face_2)
print("Result:", result_2)