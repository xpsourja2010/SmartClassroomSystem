class StudentAttendance:
    def __init__(self, student_database, attendance_register):
        self.student_database = student_database
        self.attendance_register = attendance_register

    def get_daily_register(self, attendance_date=None):
        students = self.student_database.get_all_students()
        attendance_records = (
            self.attendance_register.get_daily_attendance(
                attendance_date
            )
        )

        attendance_map = {
            record[0]: record
            for record in attendance_records
        }

        register = []

        for student in students:
            student_id = student["student_id"]
            name = student["name"]

            if student_id in attendance_map:
                record = attendance_map[student_id]

                register.append({
                    "student_id": student_id,
                    "name": name,
                    "status": record[2],
                    "timestamp": record[3]
                })

            else:
                register.append({
                    "student_id": student_id,
                    "name": name,
                    "status": "ABSENT",
                    "timestamp": None
                })

        return register

    def get_present_count(self, attendance_date=None):
        register = self.get_daily_register(attendance_date)

        return sum(
            1
            for student in register
            if student["status"] == "PRESENT"
        )

    def get_absent_count(self, attendance_date=None):
        register = self.get_daily_register(attendance_date)

        return sum(
            1
            for student in register
            if student["status"] == "ABSENT"
        )

    def get_late_count(self, attendance_date=None):
        register = self.get_daily_register(attendance_date)

        return sum(
            1
            for student in register
            if student["status"] == "LATE"
        )