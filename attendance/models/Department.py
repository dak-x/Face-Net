from datetime import datetime
from attendance import db, login_manage
from flask_login import UserMixin

class Department(db.Model):
   Dept_ID = db.Column(db.Integer,nullable=False)
   Name = db.Column(db.String(60),nullable=False)
