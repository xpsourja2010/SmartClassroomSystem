import cv2

from config import CAMERA_INDEX, CAMERA_WIDTH, CAMERA_HEIGHT


class DroidCam:
    def __init__(
        self,
        camera_index=CAMERA_INDEX,
        width=CAMERA_WIDTH,
        height=CAMERA_HEIGHT
    ):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(
            self.camera_index,
            cv2.CAP_DSHOW
        )

        if not self.cap.isOpened():
            raise RuntimeError(
                f"Could not open camera index {self.camera_index}"
            )

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        return True

    def read(self):
        if self.cap is None:
            raise RuntimeError("Camera is not open.")

        ret, frame = self.cap.read()

        if not ret:
            return None

        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None