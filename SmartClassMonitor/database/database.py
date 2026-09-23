import sqlite3
from pathlib import Path
from datetime import datetime


class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path(__file__).resolve().parent / "classroom.db"

        self.db_path = str(db_path)
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def initialize(self):
        if self.connection is None:
            self.connect()

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                name TEXT,
                status TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                attendance_date TEXT NOT NULL,
                UNIQUE(student_id, attendance_date)
            )
        """)

        self.connection.commit()

    def add_attendance(self, student_id, name, status, timestamp=None):
        if self.connection is None:
            self.connect()

        if timestamp is None:
            timestamp = datetime.now()

        attendance_date = timestamp.strftime("%Y-%m-%d")
        timestamp_text = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO attendance
            (student_id, name, status, timestamp, attendance_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            student_id,
            name,
            status,
            timestamp_text,
            attendance_date
        ))

        self.connection.commit()

        return cursor.rowcount == 1

    def get_all_attendance(self):
        if self.connection is None:
            self.connect()

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT student_id, name, status, timestamp
            FROM attendance
            ORDER BY timestamp
        """)

        return cursor.fetchall()

    def get_attendance_by_date(self, attendance_date):
        if self.connection is None:
            self.connect()

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT student_id, name, status, timestamp
            FROM attendance
            WHERE attendance_date = ?
            ORDER BY timestamp
        """, (attendance_date,))

        return cursor.fetchall()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None