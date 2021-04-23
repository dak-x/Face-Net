from datetime import datetime
from attendance import db, login_manage
from flask_login import UserMixin

class Staff(db.Model):
   Emp_ID = db.Column(db.Integer,nullable=False)
   Name = db.Column(db.String(60),nullable=False)
   Phone = db.Column(db.String(10),nullable=False)
   Email = db.Column(db.String(30),nullable=False)
   Salary = db.Column(db.Integer,nullable=False)
   Designation = db.Column(db.String(30),nullable=False)
   Dept_ID = db.Column(db.Integer,nullable=False)
   Path = db.Column(db.String(100),nullable=False)
