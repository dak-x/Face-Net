from datetime import datetime
from attendance import db, login_manage


class Employee_Attendance(db.Model):
   Emp_ID = db.Column(db.String(20),nullable=False)
   timein = db.Column(db.DateTime,nullable=False)
   timeout = db.Column(db.DateTime,nullable=False)
