from datetime import datetime


class AttendanceRegister:
    def __init__(self, database):
        self.database = database

    def get_daily_attendance(self, attendance_date=None):
        if attendance_date is None:
            attendance_date = datetime.now().strftime("%Y-%m-%d")

        return self.database.get_attendance_by_date(attendance_date)

    def get_student_attendance(self, student_id, attendance_date=None):
        records = self.get_daily_attendance(attendance_date)

        for record in records:
            if record[0] == student_id:
                return record

        return None

    def is_student_present(self, student_id, attendance_date=None):
        record = self.get_student_attendance(
            student_id,
            attendance_date
        )

        return record is not None

    def get_present_students(self, attendance_date=None):
        records = self.get_daily_attendance(attendance_date)

        return [
            record
            for record in records
            if record[2] == "PRESENT"
        ]

    def get_late_students(self, attendance_date=None):
        records = self.get_daily_attendance(attendance_date)

        return [
            record
            for record in records
            if record[2] == "LATE"
        ]