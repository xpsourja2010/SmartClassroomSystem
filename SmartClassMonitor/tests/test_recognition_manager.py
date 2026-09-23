import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from recognition.recognition_manager import RecognitionManager


manager = RecognitionManager()

face_1 = cv2.imread("tests/test_face_1.jpg")

if face_1 is None:
    print("ERROR: test_face_1.jpg not found.")
    sys.exit()

print("Registering student_001...")

if manager.register_face("student_001", face_1):
    print("Registration successful.")
else:
    print("ERROR: Face registration failed.")
    sys.exit()

print("Recognizing face...")

student_id = manager.recognize_face(face_1)

print("Recognized:", student_id)

if student_id == "student_001":
    print("Recognition manager test PASSED.")
else:
    print("Recognition manager test FAILED.")