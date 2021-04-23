from datetime import datetime
from attendance import db, login_manage
from flask_login import UserMixin

class Course(db.Model):
   Course_ID = db.Column(db.Integer,nullable=False)
   Name = db.Column(db.String(60),nullable=False)
   Semester = db.Column(db.Integer,nullable=False)
   Credit_Hour = db.Column(db.Integer,nullable=False)
