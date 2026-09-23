from datetime import datetime, timedelta


class LateDetector:
    def __init__(self, late_after_minutes=5):
        self.late_after_minutes = late_after_minutes

    def is_late(self, class_start_time, current_time=None):
        if current_time is None:
            current_time = datetime.now()

        late_time = (
            class_start_time
            + timedelta(minutes=self.late_after_minutes)
        )

        return current_time > late_time