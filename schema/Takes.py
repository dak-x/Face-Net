from datetime import datetime
from attendance import db, login_manage


class Takes(db.Model):
   Stud_Id = db.Column(db.String(20),nullable=False)
   Course_ID = db.Column(db.String(10),nullable=False)
