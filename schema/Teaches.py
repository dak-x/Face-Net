from datetime import datetime
from attendance import db, login_manage


class Teaches(db.Model):
   Faculty_ID = db.Column(db.String(20),nullable=False)
   Course_ID = db.Column(db.String(10),nullable=False)
