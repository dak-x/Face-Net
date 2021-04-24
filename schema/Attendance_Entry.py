from datetime import datetime
from attendance import db, login_manage


class Attendance_Entry(db.Model):
   Course_ID = db.Column(db.String(10),nullable=False)
   Date = db.Column(db.Integer,nullable=False)
   Semester = db.Column(db.Integer,nullable=False)
   User_ID = db.Column(db.String(20),nullable=False)
