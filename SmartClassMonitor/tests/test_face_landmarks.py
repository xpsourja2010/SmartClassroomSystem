import cv2
from insightface.app import FaceAnalysis


def main():
    app = FaceAnalysis(
        name="buffalo_l",
        providers=["CPUExecutionProvider"]
    )

    app.prepare(
        ctx_id=0,
        det_size=(640, 640)
    )

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("ERROR: Could not open camera.")
        return

    print("Camera started.")
    print("Show your face to the camera.")
    print("Press Q to stop.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("ERROR: Could not read frame.")
            break

        faces = app.get(frame)

        for face in faces:
            print("Face detected")
            print("Keypoints:")
            print(face.kps)

            for x, y in face.kps:
                cv2.circle(
                    frame,
                    (int(x), int(y)),
                    5,
                    (0, 255, 0),
                    -1
                )

        cv2.imshow("InsightFace Face Landmarks", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()