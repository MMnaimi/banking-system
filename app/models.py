from flask import render_template
from app import db,login_manager
from app.forms import RegisterationForm
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
    password = db.Column(db.String(16), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='normal')
    gender = db.Column(db.String(10), nullable=False)
    phone =  db.Column(db.String, nullable=False)
    birth_date = db.Column(db.String(50))
    def __init__(self, fullname, username , email, password, gender, phone, birth_date, state=False, role='normal' ):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.state = state
        self.password = password
        self.role = role
        self.gender = gender
        self.phone = phone
        self.birth_date = birth_date

class Account(db.Model, UserMixin):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer,primary_key=True)
    account_no = db.Column(db.String(30), nullable = False)
    acc_status = db.Column(db.Boolean, nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    def __init__(self, account_no, acc_status , balance):
        self.account_no = account_no
        self.balance = balance
        self.acc_status = acc_status

        

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key = True)
    tran_type = db.Column(db.String(30), nullable = False)
    tran_date = db.Column(db.String(30), nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))

