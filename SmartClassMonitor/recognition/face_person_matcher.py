import math


class FacePersonMatcher:
    def __init__(self, max_distance_ratio=0.6):
        self.max_distance_ratio = max_distance_ratio

    def match(self, face_bbox, tracked_people):
        fx1, fy1, fx2, fy2 = face_bbox

        face_center_x = (fx1 + fx2) / 2
        face_center_y = (fy1 + fy2) / 2

        best_person = None
        best_distance = float("inf")

        for person in tracked_people:
            px1, py1, px2, py2 = person["bbox"]

            person_width = px2 - px1
            person_height = py2 - py1

            if person_width <= 0 or person_height <= 0:
                continue

            # Face center should be inside the upper part of the person's box.
            upper_limit = py1 + person_height * 0.55

            if not (
                px1 <= face_center_x <= px2
                and py1 <= face_center_y <= upper_limit
            ):
                continue

            person_center_x = (px1 + px2) / 2
            person_center_y = py1 + person_height * 0.25

            distance = math.sqrt(
                (face_center_x - person_center_x) ** 2
                + (face_center_y - person_center_y) ** 2
            )

            max_distance = person_height * self.max_distance_ratio

            if distance <= max_distance and distance < best_distance:
                best_distance = distance
                best_person = person

        return best_person