from datetime import datetime


class AttendanceManager:
    def __init__(self, late_after_minutes=5, database=None):
        self.late_after_minutes = late_after_minutes
        self.records = {}
        self.database = database

    def mark_present(
        self,
        student_id,
        student_name=None,
        timestamp=None
    ):
        if student_id in self.records:
            return self.records[student_id]

        if timestamp is None:
            timestamp = datetime.now()

        record = {
            "student_id": student_id,
            "name": student_name,
            "status": "PRESENT",
            "time": timestamp
        }

        self.records[student_id] = record

        # Save to database if connected
        if self.database is not None:
            self.database.add_attendance(
                student_id,
                student_name,
                "PRESENT",
                timestamp
            )

        return record

    def mark_late(
        self,
        student_id,
        student_name=None,
        timestamp=None
    ):
        if student_id in self.records:
            return self.records[student_id]

        if timestamp is None:
            timestamp = datetime.now()

        record = {
            "student_id": student_id,
            "name": student_name,
            "status": "LATE",
            "time": timestamp
        }

        self.records[student_id] = record

        # Save to database if connected
        if self.database is not None:
            self.database.add_attendance(
                student_id,
                student_name,
                "LATE",
                timestamp
            )

        return record

    def get_attendance(self, student_id):
        return self.records.get(student_id)

    def get_all_attendance(self):
        return list(self.records.values())

    def is_present(self, student_id):
        return student_id in self.records

    def clear(self):
        self.records.clear()