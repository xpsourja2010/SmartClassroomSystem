import cv2
import numpy as np
import onnxruntime as ort


class LipLandmarkDetector:

    def __init__(
        self,
        model_path=r"C:\Users\U S E R\.insightface\models\buffalo_l\2d106det.onnx"
    ):
        self.session = ort.InferenceSession(
            model_path,
            providers=["CPUExecutionProvider"]
        )

        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def get_landmarks(self, face_image):

        if face_image is None or face_image.size == 0:
            return None

        # 192 x 192 input
        image = cv2.resize(face_image, (192, 192))

        # BGR -> RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # float32
        image = image.astype(np.float32)

        # InsightFace-style normalization
        image = (image - 127.5) / 128.0

        # HWC -> CHW
        image = np.transpose(image, (2, 0, 1))

        # Add batch
        image = np.expand_dims(image, axis=0).astype(np.float32)

        # Inference
        output = self.session.run(
            [self.output_name],
            {self.input_name: image}
        )[0]

        # 212 = 106 x 2
        landmarks = output.reshape(106, 2).copy()

        return landmarks

    def convert_to_image_coordinates(
        self,
        landmarks,
        crop_width,
        crop_height
    ):

        if landmarks is None:
            return None

        points = landmarks.copy()

        # Model outputs coordinates approximately
        # around the normalized [-0.5, +0.5] range.
        #
        # Convert to crop coordinates.

        points[:, 0] = (
            points[:, 0] + 0.5
        ) * crop_width

        points[:, 1] = (
            points[:, 1] + 0.5
        ) * crop_height

        return points