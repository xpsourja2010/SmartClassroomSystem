import sys
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

import cv2

from camera.droidcam import DroidCam
from detection.vision_pipeline import VisionPipeline
from recognition.recognition_manager import RecognitionManager
from recognition.face_person_matcher import FacePersonMatcher
from attendance.attendance import AttendanceManager
from database.database import Database


# ============================================================
# SETTINGS
# ============================================================

FACE_RECOGNITION_INTERVAL = 15
FACE_THRESHOLD = 0.45


# ============================================================
# FACE IMAGE PATHS
# ============================================================

TESTS_FOLDER = Path(__file__).resolve().parent

FACE_1_PATH = TESTS_FOLDER / "test_face_1.jpg"
FACE_2_PATH = TESTS_FOLDER / "test_face_2.jpg"
FACE_3_PATH = TESTS_FOLDER / "test_face_3.jpg"


# ============================================================
# LOAD FACE IMAGES
# ============================================================

face_1 = cv2.imread(str(FACE_1_PATH))
face_2 = cv2.imread(str(FACE_2_PATH))
face_3 = cv2.imread(str(FACE_3_PATH))

if face_1 is None:
    raise RuntimeError(f"Could not load {FACE_1_PATH}")

if face_2 is None:
    raise RuntimeError(f"Could not load {FACE_2_PATH}")

if face_3 is None:
    raise RuntimeError(f"Could not load {FACE_3_PATH}")


# ============================================================
# DATABASE
# ============================================================

database = Database("database/classroom.db")
database.initialize()


# ============================================================
# CAMERA
# ============================================================

camera = DroidCam()
camera.open()


# ============================================================
# VISION PIPELINE
# ============================================================

vision = VisionPipeline()


# ============================================================
# FACE RECOGNITION
# ============================================================

recognition = RecognitionManager()
matcher = FacePersonMatcher()


# ============================================================
# ATTENDANCE CONNECTED TO DATABASE
# ============================================================

attendance = AttendanceManager(
    database=database
)


# ============================================================
# REGISTER STUDENTS
# ============================================================

if not recognition.register_face("student_001", face_1):
    raise RuntimeError("Could not register student_001")

if not recognition.register_face("student_002", face_2):
    raise RuntimeError("Could not register student_002")

if not recognition.register_face("student_003", face_3):
    raise RuntimeError("Could not register student_003")


student_names = {
    "student_001": "Student 1",
    "student_002": "Student 2",
    "student_003": "Student 3"
}


# ============================================================
# IDENTITY STORAGE
# ============================================================

identity_map = {}
identity_score_map = {}


# ============================================================
# START MESSAGE
# ============================================================

print()
print("==============================================")
print(" SmartClassMonitor Live Attendance Demo")
print("==============================================")
print()
print("Registered students:")
print("student_001 - Student 1")
print("student_002 - Student 2")
print("student_003 - Student 3")
print()
print("SQLite database: database/classroom.db")
print(f"Face recognition: every {FACE_RECOGNITION_INTERVAL} frames")
print(f"Face threshold: {FACE_THRESHOLD}")
print()
print("Segmentation + Pose + Tracking enabled.")
print("Attendance → SQLite enabled.")
print("Press Q to stop.")
print()


# ============================================================
# MAIN LOOP
# ============================================================

frame_count = 0

try:

    while True:

        # ----------------------------------------------------
        # READ CAMERA
        # ----------------------------------------------------

        frame = camera.read()

        if frame is None:
            print("ERROR: Could not read camera frame.")
            break

        frame_count += 1


        # ----------------------------------------------------
        # VISION PIPELINE
        # ----------------------------------------------------

        output, tracked_people = vision.process(frame)


        # ----------------------------------------------------
        # FACE RECOGNITION
        # ----------------------------------------------------

        if frame_count % FACE_RECOGNITION_INTERVAL == 0:

            faces = recognition.recognizer.app.get(frame)

            for face in faces:

                bbox = face.bbox.astype(int)

                fx1, fy1, fx2, fy2 = bbox.tolist()

                matched_person = matcher.match(
                    (fx1, fy1, fx2, fy2),
                    tracked_people
                )

                if matched_person is None:
                    continue

                track_id = matched_person["id"]

                if track_id is None:
                    continue


                # ------------------------------------------------
                # RECOGNIZE FACE
                # ------------------------------------------------

                student_id = recognition.recognizer.recognize_embedding(
                    face.embedding,
                    threshold=FACE_THRESHOLD
                )


                # ------------------------------------------------
                # KNOWN STUDENT
                # ------------------------------------------------

                if student_id is not None:

                    identity_map[track_id] = student_id

                    known_embedding = (
                        recognition.recognizer.known_faces[student_id]
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


                # ------------------------------------------------
                # UNKNOWN
                # ------------------------------------------------

                else:

                    identity_map[track_id] = "Unknown"
                    identity_score_map[track_id] = 0.0


        # ====================================================
        # DRAW TRACKS + ATTENDANCE
        # ====================================================

        for person in tracked_people:

            track_id = person["id"]

            x1, y1, x2, y2 = map(
                int,
                person["bbox"]
            )

            student_id = identity_map.get(
                track_id,
                "Unknown"
            )

            score = identity_score_map.get(
                track_id,
                0.0
            )


            # ------------------------------------------------
            # ATTENDANCE
            # ------------------------------------------------

            if student_id != "Unknown":

                student_name = student_names.get(
                    student_id,
                    student_id
                )

                was_present_before = attendance.is_present(
                    student_id
                )

                record = attendance.mark_present(
                    student_id,
                    student_name
                )

                if not was_present_before:

                    print(
                        f"ATTENDANCE SAVED: "
                        f"{student_id} - "
                        f"{student_name} - "
                        f"PRESENT - "
                        f"{record['time']}"
                    )


            # ------------------------------------------------
            # LABEL
            # ------------------------------------------------

            if student_id == "Unknown":

                label = f"Track {track_id}: Unknown"

            else:

                label = (
                    f"Track {track_id}: "
                    f"{student_id} "
                    f"({score:.2f})"
                )


            # ------------------------------------------------
            # READABLE LABEL
            # ------------------------------------------------

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.65
            thickness = 2

            (text_width, text_height), _ = cv2.getTextSize(
                label,
                font,
                font_scale,
                thickness
            )

            label_x = max(x1, 5)

            label_y = max(
                y1 - 12,
                text_height + 15
            )


            # ------------------------------------------------
            # LABEL BACKGROUND
            # ------------------------------------------------

            cv2.rectangle(
                output,
                (
                    label_x,
                    label_y - text_height - 10
                ),
                (
                    label_x + text_width + 12,
                    label_y + 5
                ),
                (0, 0, 0),
                -1
            )


            # ------------------------------------------------
            # LABEL TEXT
            # ------------------------------------------------

            cv2.putText(
                output,
                label,
                (
                    label_x + 6,
                    label_y
                ),
                font,
                font_scale,
                (255, 255, 255),
                thickness,
                cv2.LINE_AA
            )


        # ====================================================
        # ATTENDANCE COUNTER
        # ====================================================

        present_count = len(
            attendance.get_all_attendance()
        )

        counter_text = f"Present: {present_count}/3"

        counter_font = cv2.FONT_HERSHEY_SIMPLEX
        counter_scale = 0.8
        counter_thickness = 2

        (
            counter_width,
            counter_height
        ), _ = cv2.getTextSize(
            counter_text,
            counter_font,
            counter_scale,
            counter_thickness
        )


        cv2.rectangle(
            output,
            (10, 10),
            (
                counter_width + 25,
                counter_height + 25
            ),
            (0, 0, 0),
            -1
        )


        cv2.putText(
            output,
            counter_text,
            (18, counter_height + 18),
            counter_font,
            counter_scale,
            (255, 255, 255),
            counter_thickness,
            cv2.LINE_AA
        )


        # ====================================================
        # DISPLAY
        # ====================================================

        cv2.imshow(
            "SmartClassMonitor - Live Attendance",
            output
        )


        # ====================================================
        # QUIT
        # ====================================================

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


finally:

    camera.release()
    cv2.destroyAllWindows()
    database.close()


# ============================================================
# FINAL ATTENDANCE FROM DATABASE
# ============================================================

print()
print("==============================================")
print(" DATABASE ATTENDANCE")
print("==============================================")

records = database.get_all_attendance()

if not records:

    print("No attendance recorded.")

else:

    for record in records:

        print(
            f"{record[0]} | "
            f"{record[1]} | "
            f"{record[2]} | "
            f"{record[3]}"
        )

print("==============================================")
print("Live attendance → SQLite test complete.")