import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from camera.droidcam import DroidCam
from detection.vision_pipeline import VisionPipeline
from recognition.recognition_manager import RecognitionManager
from recognition.face_person_matcher import FacePersonMatcher


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

FACE_RECOGNITION_INTERVAL = 15
FACE_THRESHOLD = 0.45


# --------------------------------------------------
# INITIALIZE
# --------------------------------------------------

camera = DroidCam()
vision = VisionPipeline()
recognition = RecognitionManager()
matcher = FacePersonMatcher()


# --------------------------------------------------
# LOAD REGISTERED FACES
# --------------------------------------------------

face_1 = cv2.imread("tests/test_face_1.jpg")
face_2 = cv2.imread("tests/test_face_2.jpg")

if face_1 is None or face_2 is None:
    print("ERROR: Test face images not found.")
    sys.exit()


# --------------------------------------------------
# REGISTER STUDENTS
# --------------------------------------------------

if not recognition.register_face("student_001", face_1):
    print("ERROR: Could not register student_001.")
    sys.exit()

if not recognition.register_face("student_002", face_2):
    print("ERROR: Could not register student_002.")
    sys.exit()


print("Identity pipeline loaded.")
print(
    f"Face recognition interval: "
    f"every {FACE_RECOGNITION_INTERVAL} frames"
)
print("Press Q to stop.")


# --------------------------------------------------
# START CAMERA
# --------------------------------------------------

camera.open()

frame_count = 0

# Track ID -> recognized student
identity_map = {}

# Track ID -> confidence
identity_score_map = {}


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

while True:

    frame = camera.read()

    if frame is None:
        print("ERROR: Could not read camera frame.")
        break

    frame_count += 1


    # --------------------------------------------------
    # PERSON SEGMENTATION + POSE + TRACKING
    # --------------------------------------------------

    output, tracked_people = vision.process(frame)


    # Current tracking IDs
    current_track_ids = {
        person["id"]
        for person in tracked_people
        if person["id"] is not None
    }


    # Remove identities belonging to people
    # who are no longer being tracked.
    for track_id in list(identity_map.keys()):

        if track_id not in current_track_ids:
            del identity_map[track_id]

            if track_id in identity_score_map:
                del identity_score_map[track_id]


    # --------------------------------------------------
    # RUN INSIGHTFACE PERIODICALLY
    # --------------------------------------------------

    should_recognize = (
        frame_count % FACE_RECOGNITION_INTERVAL == 0
    )


    if should_recognize:

        faces = recognition.recognizer.app.get(frame)

        for face in faces:

            fx1, fy1, fx2, fy2 = map(
                int,
                face.bbox
            )


            # ------------------------------------------
            # MATCH FACE TO TRACKED PERSON
            # ------------------------------------------

            matched_person = matcher.match(
                (fx1, fy1, fx2, fy2),
                tracked_people
            )


            if matched_person is None:
                continue


            track_id = matched_person["id"]


            # ------------------------------------------
            # RECOGNIZE USING EXISTING EMBEDDING
            # ------------------------------------------

            student_id = (
                recognition.recognizer.recognize_embedding(
                    face.embedding,
                    threshold=FACE_THRESHOLD
                )
            )


            if student_id is not None:

                identity_map[track_id] = student_id

                # Calculate similarity score
                known_embedding = (
                    recognition.recognizer
                    .known_faces[student_id]
                )

                current_embedding = face.embedding
                current_embedding = (
                    current_embedding /
                    (current_embedding @ current_embedding) ** 0.5
                )

                score = float(
                    current_embedding @ known_embedding
                )

                identity_score_map[track_id] = score

            else:

                identity_map[track_id] = "Unknown"
                identity_score_map[track_id] = 0.0


    # --------------------------------------------------
    # DRAW TRACK + IDENTITY
    # --------------------------------------------------

    for person in tracked_people:

        track_id = person["id"]

        if track_id is None:
            continue


        x1, y1, x2, y2 = map(
            int,
            person["bbox"]
        )


        # ------------------------------------------
        # GET CACHED IDENTITY
        # ------------------------------------------

        student_id = identity_map.get(
            track_id,
            "Recognizing..."
        )

        score = identity_score_map.get(
            track_id,
            0.0
        )


        if student_id == "Recognizing...":

            label = (
                f"Track {track_id}: "
                "Recognizing..."
            )

        elif student_id == "Unknown":

            label = (
                f"Track {track_id}: "
                f"Unknown"
            )

        else:

            label = (
                f"Track {track_id}: "
                f"{student_id} "
                f"({score:.2f})"
            )


        # ------------------------------------------
        # DRAW IDENTITY LABEL
        # ------------------------------------------

        cv2.putText(
            output,
            label,
            (x1, max(y1 - 12, 25)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2
        )


        # ------------------------------------------
        # DRAW TRACK BOX
        # ------------------------------------------

        cv2.rectangle(
            output,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            1
        )


    # --------------------------------------------------
    # DISPLAY
    # --------------------------------------------------

    cv2.imshow(
        "SmartClassMonitor - Optimized Identity Pipeline",
        output
    )


    # --------------------------------------------------
    # QUIT
    # --------------------------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------------------------
# CLEANUP
# --------------------------------------------------

camera.release()
cv2.destroyAllWindows()