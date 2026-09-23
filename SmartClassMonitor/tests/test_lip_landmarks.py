import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

import cv2

from detection.face_detection import FaceDetector
from behaviour.lip_landmarks import LipLandmarkDetector


FACE_MODEL = "yolov12n-face.pt"

LANDMARK_MODEL = (
    r"C:\Users\U S E R\.insightface\models\buffalo_l\2d106det.onnx"
)


def main():

    face_detector = FaceDetector(FACE_MODEL)

    landmark_detector = LipLandmarkDetector(
        LANDMARK_MODEL
    )

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open camera.")
        return

    print("YOLO Face + InsightFace 106 Landmark Test")
    print("Press Q to quit.")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        faces = face_detector.detect(frame)

        for face in faces:

            x, y, w, h = face["bbox"]
            confidence = face["confidence"]

            # -----------------------------------------
            # Face bounding box
            # -----------------------------------------

            x1 = max(0, x)
            y1 = max(0, y)
            x2 = min(frame.shape[1], x + w)
            y2 = min(frame.shape[0], y + h)

            if x2 <= x1 or y2 <= y1:
                continue

            # -----------------------------------------
            # Loose crop
            # -----------------------------------------

            pad_x = int((x2 - x1) * 0.20)
            pad_y = int((y2 - y1) * 0.20)

            cx1 = max(0, x1 - pad_x)
            cy1 = max(0, y1 - pad_y)

            cx2 = min(
                frame.shape[1],
                x2 + pad_x
            )

            cy2 = min(
                frame.shape[0],
                y2 + pad_y
            )

            face_crop = frame[
                cy1:cy2,
                cx1:cx2
            ]

            if face_crop.size == 0:
                continue

            # -----------------------------------------
            # 106 landmarks
            # -----------------------------------------

            landmarks = landmark_detector.get_landmarks(
                face_crop
            )

            if landmarks is None:
                continue

            crop_h, crop_w = face_crop.shape[:2]

            points = landmark_detector.convert_to_image_coordinates(
                landmarks,
                crop_w,
                crop_h
            )

            # -----------------------------------------
            # Draw landmarks
            # -----------------------------------------

            for px, py in points:

                px = int(px) + cx1
                py = int(py) + cy1

                if (
                    0 <= px < frame.shape[1]
                    and 0 <= py < frame.shape[0]
                ):

                    cv2.circle(
                        frame,
                        (px, py),
                        2,
                        (0, 255, 0),
                        -1
                    )

            # -----------------------------------------
            # Face box
            # -----------------------------------------

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                f"Face {confidence:.2f}",
                (x1, max(25, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

        cv2.imshow(
            "SmartClassMonitor - 106 Landmarks",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()