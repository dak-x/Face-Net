
from attendance import db, login_manage


class Course(db.Model):
    Course_ID = db.Column(db.String(10),nullable=False)
    Name = db.Column(db.String(60),nullable=False)
    Semester = db.Column(db.Integer,nullable=False)
    Credit_Hour = db.Column(db.Integer,nullable=False)
