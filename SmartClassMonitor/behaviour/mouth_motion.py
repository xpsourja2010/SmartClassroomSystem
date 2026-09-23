import cv2
import numpy as np


class MouthMotionDetector:
    def __init__(
        self,
        opening_threshold=0.10,
        closing_threshold=0.07,
        required_cycles=2,
        max_idle_frames=12,
        min_cycle_gap=0
    ):
        self.opening_threshold = opening_threshold
        self.closing_threshold = closing_threshold
        self.required_cycles = required_cycles
        self.max_idle_frames = max_idle_frames
        self.min_cycle_gap = min_cycle_gap

        self.previous_mouth = {}
        self.previous_state = {}
        self.cycle_count = {}
        self.idle_frames = {}
        self.cycle_gap = {}
        self.talking_state = {}

    def _get_mouth_roi(self, frame, face_bbox):
        x1, y1, x2, y2 = face_bbox

        width = x2 - x1
        height = y2 - y1

        if width <= 0 or height <= 0:
            return None

        # Mouth region inside the lower half of the face.
        roi_x1 = int(x1 + width * 0.20)
        roi_x2 = int(x1 + width * 0.80)

        roi_y1 = int(y1 + height * 0.50)
        roi_y2 = int(y1 + height * 0.88)

        h, w = frame.shape[:2]

        roi_x1 = max(0, min(roi_x1, w - 1))
        roi_x2 = max(0, min(roi_x2, w))

        roi_y1 = max(0, min(roi_y1, h - 1))
        roi_y2 = max(0, min(roi_y2, h))

        if roi_x2 <= roi_x1 or roi_y2 <= roi_y1:
            return None

        roi = frame[
            roi_y1:roi_y2,
            roi_x1:roi_x2
        ]

        if roi.size == 0:
            return None

        roi = cv2.resize(roi, (64, 48))
        roi = cv2.cvtColor(
            roi,
            cv2.COLOR_BGR2GRAY
        )

        return roi

    def _calculate_opening(self, roi):
        if roi is None:
            return 0.0

        # Dark-pixel ratio.
        _, threshold = cv2.threshold(
            roi,
            80,
            255,
            cv2.THRESH_BINARY_INV
        )

        dark_pixels = np.sum(threshold > 0)
        total_pixels = threshold.size

        if total_pixels == 0:
            return 0.0

        return dark_pixels / total_pixels

    def detect(self, frame, face_bbox, person_id):

        roi = self._get_mouth_roi(
            frame,
            face_bbox
        )

        if roi is None:
            self.reset(person_id)

            return {
                "opening": 0.0,
                "talking": False,
                "cycle": False
            }

        opening = self._calculate_opening(roi)

        previous_state = self.previous_state.get(
            person_id,
            "closed"
        )

        cycles = self.cycle_count.get(
            person_id,
            0
        )

        idle = self.idle_frames.get(
            person_id,
            0
        )

        gap = self.cycle_gap.get(
            person_id,
            self.min_cycle_gap
        )

        cycle = False

        # ------------------------------------------
        # GAP CONTROL
        # ------------------------------------------

        if gap < self.min_cycle_gap:
            gap += 1

        # ------------------------------------------
        # OPENING DETECTION
        # ------------------------------------------
        #
        # IMPORTANT:
        # We now use the actual opening value,
        # NOT frame-to-frame difference.
        #

        if (
            opening >= self.opening_threshold
            and previous_state == "closed"
            and gap >= self.min_cycle_gap
        ):
            previous_state = "open"
            idle = 0

        # ------------------------------------------
        # CLOSING DETECTION
        # ------------------------------------------

        elif (
            opening <= self.closing_threshold
            and previous_state == "open"
        ):
            previous_state = "closed"

            cycles += 1
            cycle = True

            gap = 0
            idle = 0

        else:
            idle += 1

        # ------------------------------------------
        # RESET OLD ACTIVITY
        # ------------------------------------------

        if idle > self.max_idle_frames:
            cycles = 0
            previous_state = "closed"

        # ------------------------------------------
        # TALKING
        # ------------------------------------------

        talking = cycles >= self.required_cycles

        if idle > self.max_idle_frames:
            talking = False

        # ------------------------------------------
        # SAVE STATE
        # ------------------------------------------

        self.previous_mouth[person_id] = opening
        self.previous_state[person_id] = previous_state
        self.cycle_count[person_id] = cycles
        self.idle_frames[person_id] = idle
        self.cycle_gap[person_id] = gap
        self.talking_state[person_id] = talking

        return {
            "opening": opening,
            "talking": talking,
            "cycle": cycle
        }

    def get_state(self, person_id):
        return self.talking_state.get(
            person_id,
            False
        )

    def reset(self, person_id):
        self.previous_mouth.pop(person_id, None)
        self.previous_state.pop(person_id, None)
        self.cycle_count.pop(person_id, None)
        self.idle_frames.pop(person_id, None)
        self.cycle_gap.pop(person_id, None)
        self.talking_state.pop(person_id, None)

    def clear(self):
        self.previous_mouth.clear()
        self.previous_state.clear()
        self.cycle_count.clear()
        self.idle_frames.clear()
        self.cycle_gap.clear()
        self.talking_state.clear()