class PersonTracker:

    def __init__(self):
        self.tracked_people = {}

    def update(self, tracking_result):
        """
        Extract person tracking information
        from a YOLO tracking result.
        """

        tracked_people = []

        if tracking_result.boxes is None:
            self.tracked_people = {}
            return tracked_people

        boxes = tracking_result.boxes

        ids = boxes.id
        coordinates = boxes.xyxy
        confidences = boxes.conf
        classes = boxes.cls

        for index in range(len(boxes)):

            track_id = None

            if ids is not None:
                track_id = int(ids[index].item())

            x1, y1, x2, y2 = coordinates[index].tolist()

            confidence = float(
                confidences[index].item()
            )

            class_id = int(
                classes[index].item()
            )

            width = x2 - x1
            height = y2 - y1

            center_x = x1 + width / 2
            center_y = y1 + height / 2

            person = {
                "track_id": track_id,

                "bbox": (
                    x1,
                    y1,
                    x2,
                    y2
                ),

                "center": (
                    center_x,
                    center_y
                ),

                "width": width,
                "height": height,

                "confidence": confidence,

                "class_id": class_id
            }

            tracked_people.append(person)

        self.tracked_people = {
            person["track_id"]: person
            for person in tracked_people
            if person["track_id"] is not None
        }

        return tracked_people

    def get_person(self, track_id):
        """
        Get a currently tracked person by
        temporary YOLO track ID.
        """

        return self.tracked_people.get(track_id)

    def get_all(self):
        """
        Return all currently tracked people.
        """

        return list(self.tracked_people.values())

    def reset(self):
        """
        Clear current tracking information.
        """

        self.tracked_people.clear()
