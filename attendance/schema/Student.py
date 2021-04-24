from datetime import datetime
from attendance import db, login_manage


class Student(db.Model):
   Stud_ID = db.Column(db.String(20),nullable=False)
   Name = db.Column(db.String(60),nullable=False)
   DOB = db.Column(db.Integer,nullable=False)
   Email = db.Column(db.String(30),nullable=False)
   Phone = db.Column(db.String(10),nullable=False)
   Gender = db.Column(db.String(1),nullable=False)
   Semester = db.Column(db.Integer,nullable=False)
   Dept_ID = db.Column(db.String(10),nullable=False)
   Path = db.Column(db.String(100),nullable=False)
