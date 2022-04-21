from flask import render_template
from app import db,login_manager
from app.forms import RegisterationForm
from datetime import datetime
from flask_login import UserMixin
from flask import render_template

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    form = RegisterationForm()
    return render_template('register.html',form=form, message = "Unauthorized Accesss, Please Register first")

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    state = db.Column(db.Boolean, nullable=False, default=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(16), nullable=False)
    role = db.Column(db.Integer, default=2)
    gender = db.Column(db.String(10), nullable=False)
    phone =  db.Column(db.String, nullable=False)
    birth_date = db.Column(db.String(50))
    def __init__(self, fullname, username , email, password, gender, phone, birth_date, state=False, balance=0, role=2 ):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.state = state
        self.balance = balance
        self.password = password
        self.role = role
        self.gender = gender
        self.phone = phone
        self.birth_date = str(birth_date)


