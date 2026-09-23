import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from recognition.face_person_matcher import FacePersonMatcher


matcher = FacePersonMatcher()

tracked_people = [
    {
        "id": 1,
        "bbox": (100, 100, 300, 500)
    },
    {
        "id": 2,
        "bbox": (400, 100, 600, 500)
    }
]

face_bbox = (150, 130, 220, 210)

matched_person = matcher.match(
    face_bbox,
    tracked_people
)

print("Matched person:")

if matched_person:
    print(matched_person)
else:
    print("None")

if matched_person and matched_person["id"] == 1:
    print("Face-person matcher test PASSED.")
else:
    print("Face-person matcher test FAILED.")