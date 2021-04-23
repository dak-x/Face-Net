from datetime import datetime
from attendance import db, login_manage
from flask_login import UserMixin

class Faculty(db.Model):
   Faculty_ID = db.Column(db.Integer,nullable=False)
   Name = db.Column(db.String(60),nullable=False)
   Role = db.Column(db.String(40),nullable=False)
   E-Mail = db.Column(db.String(30),nullable=False)
   Salary = db.Column(db.Integer,nullable=False)
   Dept_ID = db.Column(db.Integer,nullable=False)
   Path = db.Column(db.String(100),nullable=False)
