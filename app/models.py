from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    state = db.Column(db.Boolean, nullable=False, default=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(16), nullable=False)
    role = db.Column(db.Integer, default=2)
    gender = db.Column(db.String(10), nullable=False)
    phone =  db.Column(db.Integer, nullable=False)
    birth_date = db.Column(db.DateTime, default=datetime.today())

