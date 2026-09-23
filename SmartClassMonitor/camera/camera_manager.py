import cv2

from config import CAMERA_INDEX, WINDOW_NAME
from camera.droidcam import DroidCam


class CameraManager:
    def __init__(self, camera_index=CAMERA_INDEX):
        self.camera = DroidCam(camera_index=camera_index)

    def start(self):
        self.camera.open()

    def run(self):
        while True:
            frame = self.camera.read()

            if frame is None:
                print("ERROR: Could not read camera frame.")
                break

            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        self.stop()

    def stop(self):
        self.camera.release()
        cv2.destroyAllWindows()