import math


class TalkingDetector:
    def __init__(
        self,
        movement_threshold=2.5,
        required_movement_frames=3
    ):
        self.movement_threshold = movement_threshold
        self.required_movement_frames = required_movement_frames

        self.previous_mouth = {}
        self.movement_count = {}
        self.talking_state = {}

    def _distance(self, point_a, point_b):
        return math.sqrt(
            (point_a[0] - point_b[0]) ** 2
            + (point_a[1] - point_b[1]) ** 2
        )

    def detect(self, person_id, mouth_keypoints):
        """
        Detect possible talking from mouth movement.

        mouth_keypoints should contain mouth-related
        pose coordinates for one person.
        """

        if mouth_keypoints is None:
            self.talking_state[person_id] = False
            return False

        if len(mouth_keypoints) == 0:
            self.talking_state[person_id] = False
            return False

        current_mouth = mouth_keypoints[0]

        if person_id not in self.previous_mouth:
            self.previous_mouth[person_id] = current_mouth
            self.movement_count[person_id] = 0
            self.talking_state[person_id] = False
            return False

        previous_mouth = self.previous_mouth[person_id]

        movement = self._distance(
            current_mouth,
            previous_mouth
        )

        self.previous_mouth[person_id] = current_mouth

        if movement >= self.movement_threshold:
            self.movement_count[person_id] += 1
        else:
            self.movement_count[person_id] = max(
                0,
                self.movement_count[person_id] - 1
            )

        if (
            self.movement_count[person_id]
            >= self.required_movement_frames
        ):
            self.talking_state[person_id] = True
        else:
            self.talking_state[person_id] = False

        return self.talking_state[person_id]

    def get_state(self, person_id):
        return self.talking_state.get(
            person_id,
            False
        )

    def reset(self, person_id):
        self.previous_mouth.pop(person_id, None)
        self.movement_count.pop(person_id, None)
        self.talking_state.pop(person_id, None)

    def clear(self):
        self.previous_mouth.clear()
        self.movement_count.clear()
        self.talking_state.clear()