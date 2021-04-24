from datetime import datetime
from attendance import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	image_file = db.Column(db.String(20),nullable=False, default='profile.png')
	def __repr__(self):
		return "User( '{}', '{}', '{}')".format(self.username, self.email, self.password)


class Staff(db.Model):
    Emp_ID = db.Column(db.String(20),nullable=False,primary_key=True)
    Name = db.Column(db.String(60),nullable=False)
    Phone = db.Column(db.String(10),nullable=False)
    Email = db.Column(db.String(30),nullable=False)
    Salary = db.Column(db.Integer,nullable=False)
    Designation = db.Column(db.String(30),nullable=False)
    Dept_ID = db.Column(db.String(20),nullable=False)
    Path = db.Column(db.String(100),nullable=False)


class Student(db.Model):
    Stud_ID = db.Column(db.String(20),nullable=False, primary_key=True)
    Name = db.Column(db.String(60),nullable=False)
    DOB = db.Column(db.DateTime,nullable=False)
    Email = db.Column(db.String(30),nullable=False)
    Phone = db.Column(db.String(10),nullable=False)
    Gender = db.Column(db.String(1),nullable=False)
    Semester = db.Column(db.Integer,nullable=False)
    Dept_ID = db.Column(db.String(10),nullable=False)
    Path = db.Column(db.String(100),nullable=False)


class Faculty(db.Model):
    Faculty_ID = db.Column(db.String(20),nullable=False,primary_key=True)
    Name = db.Column(db.String(60),nullable=False)
    Role = db.Column(db.String(40),nullable=False)
    E-Mail = db.Column(db.String(30),nullable=False)
    Salary = db.Column(db.Integer,nullable=False)
    Dept_ID = db.Column(db.String(10),nullable=False)
    Path = db.Column(db.String(100),nullable=False)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Dept_ID = db.Column(db.String(20),nullable=False)
    Name = db.Column(db.String(60),nullable=False)


class Course(db.Model):
    Course_ID = db.Column(db.String(10),nullable=False, primary_key=True)
    Name = db.Column(db.String(60),nullable=False)
    Semester = db.Column(db.Integer,nullable=False)
    Credit_Hour = db.Column(db.Integer,nullable=False)

class Employee_Attendance(db.Model):
    Emp_ID = db.Column(db.String(20),nullable=False)
    timein = db.Column(db.DateTime,nullable=False)
    timeout = db.Column(db.DateTime,nullable=False)

class Attendance_Entry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Course_ID = db.Column(db.String(10),nullable=False)
	Date = db.Column(db.DateTime,nullable=False)
	Semester = db.Column(db.Integer,nullable=False)
	User_ID = db.Column(db.String(20),nullable=False)

class takes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Course_ID = db.Column(db.String(10),nullable=False)
	User_ID = db.Column(db.String(20),nullable=False)

class Teaches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Faculty_ID = db.Column(db.String(20),nullable=False)
    Course_ID = db.Column(db.String(10),nullable=False)

class TimeTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Course_ID = db.Column(db.String(10),nullable=False)
    Day = db.Column(db.String(20),nullable=False)
    Start_Time = db.Column(db.DateTime,nullable=False)
    End_Time = db.Column(db.DateTime,nullable=False)
    Semester = db.Column(db.Integer,nullable=False)