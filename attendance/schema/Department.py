
from attendance import db, login_manage


class Department(db.Model):
    Dept_ID = db.Column(db.String(20),nullable=False)
    Name = db.Column(db.String(60),nullable=False)
