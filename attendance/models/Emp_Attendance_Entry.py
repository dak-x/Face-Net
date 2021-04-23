from datetime import datetime
from attendance import db, login_manage
from flask_login import UserMixin

class Emp_Attendance_Entry(db.Model):
   Date = db.Column(db.Integer,nullable=False)
   Time_in = db.Column(db.Integer,nullable=False)
   Time_out = db.Column(db.Integer,nullable=False)
   Emp_ID = db.Column(db.Integer,nullable=False)
