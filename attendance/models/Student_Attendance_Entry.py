from datetime import datetime
from attendance import db, login_manage
from flask_login import UserMixin

class Student_Attendance_Entry(db.Model):
   Course_ID = db.Column(db.Integer,nullable=False)
   Date = db.Column(db.Integer,nullable=False)
   Semester = db.Column(db.Integer,nullable=False)
   Stud_ID = db.Column(db.Integer,nullable=False)