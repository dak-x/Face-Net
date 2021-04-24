
from attendance import db


class Staff(db.Model):
    Emp_ID = db.Column(db.String(20),nullable=False)
    Name = db.Column(db.String(60),nullable=False)
    Phone = db.Column(db.String(10),nullable=False)
    Email = db.Column(db.String(30),nullable=False)
    Salary = db.Column(db.Integer,nullable=False)
    Designation = db.Column(db.String(30),nullable=False)
    Dept_ID = db.Column(db.String(20),nullable=False)
    Path = db.Column(db.String(100),nullable=False)


class Student(db.Model):
    Stud_ID = db.Column(db.String(20),nullable=False)
    Name = db.Column(db.String(60),nullable=False)
    DOB = db.Column(db.DateTime,nullable=False)
    Email = db.Column(db.String(30),nullable=False)
    Phone = db.Column(db.String(10),nullable=False)
    Gender = db.Column(db.String(1),nullable=False)
    Semester = db.Column(db.Integer,nullable=False)
    Dept_ID = db.Column(db.String(10),nullable=False)
    Path = db.Column(db.String(100),nullable=False)


class Faculty(db.Model):
    Faculty_ID = db.Column(db.String(20),nullable=False)
    Name = db.Column(db.String(60),nullable=False)
    Role = db.Column(db.String(40),nullable=False)
    E-Mail = db.Column(db.String(30),nullable=False)
    Salary = db.Column(db.Integer,nullable=False)
    Dept_ID = db.Column(db.String(10),nullable=False)
    Path = db.Column(db.String(100),nullable=False)


class Department(db.Model):
    Dept_ID = db.Column(db.String(20),nullable=False)
    Name = db.Column(db.String(60),nullable=False)


class Course(db.Model):
    Course_ID = db.Column(db.String(10),nullable=False)
    Name = db.Column(db.String(60),nullable=False)
    Semester = db.Column(db.Integer,nullable=False)
    Credit_Hour = db.Column(db.Integer,nullable=False)


class Attendance_Entry(db.Model):
    Course_ID = db.Column(db.String(10),nullable=False)
    Date = db.Column(db.DateTime,nullable=False)
    Semester = db.Column(db.Integer,nullable=False)
    User_ID = db.Column(db.String(20),nullable=False)


class Employee_Attendance(db.Model):
    Emp_ID = db.Column(db.String(20),nullable=False)
    timein = db.Column(db.DateTime,nullable=False)
    timeout = db.Column(db.DateTime,nullable=False)


class Teaches(db.Model):
    Faculty_ID = db.Column(db.String(20),nullable=False)
    Course_ID = db.Column(db.String(10),nullable=False)


class Takes(db.Model):
    Stud_Id = db.Column(db.String(20),nullable=False)
    Course_ID = db.Column(db.String(10),nullable=False)
