from email import message
from flask import render_template
from app import db,login_manager
from flask_login import UserMixin
from flask import render_template

@login_manager.user_loader
def load_user(user_id):
    """
        This callback is used to reload the user object from the user ID stored in the session.
    """
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    """
        This function is used for unauthorized users.
    """
    return render_template('404.html', message = "Unauthorized Accesss, Please Register first")

class User(db.Model, UserMixin):
    """This Class represent the users table in the database.
    
    Attributes:
    -----------
    id -> int, primary key
    fullname -> str, not null
    username -> str, unique, not null
    email -> str, not null
    state -> str, not null
    password -> str, not null
    role -> str, not null
    gender -> str, not null
    phone -> str, not null
    birth_date -> str, not null
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    state = db.Column(db.String(10), nullable=False, default='pending')
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='normal')
    gender = db.Column(db.String(10), nullable=False)
    phone =  db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.String(50))
    account = db.relationship('Account', cascade="all, delete", uselist=False, backref='')
    transaction = db.relationship('Transaction', cascade='all, delete')


    def create(self, fullname, username , email, password, gender, phone, birth_date, state='pending', role='normal' ):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.state = state
        self.password = password
        self.role = role
        self.gender = gender
        self.phone = phone
        self.birth_date = birth_date
    
    
    def custom_validation(self, form):
        value = {'state':True, 'message':''}
        check_username = self.query.filter_by(username=form.username.data).first()
        check_email = self.query.filter_by(email=form.email.data).first()
        if check_username:
            value['state'] = False
            value['message'] = "Username Already Exist"
            
        elif check_email:
            value['state'] = False
            value['message'] = "Email Already Exist"
        return value



class Account(db.Model, UserMixin):
    """This Class represent the accounts table in the database.
    
    Attributes:
    -----------
    id -> int, primary key
    account_no -> str, unique, not null
    acc_status -> Boolean, not null
    balance -> int, not null, default is 0
    uid -> int, foreign key with user id
    """

    __tablename__ = 'accounts'

    id = db.Column(db.Integer,primary_key=True)
    account_no = db.Column(db.String(30), unique=True, nullable = False)
    acc_status = db.Column(db.Boolean, nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship("User", back_populates="account")
    def __init__(self, account_no, uid, balance = 0, acc_status = False):
        self.account_no = account_no
        self.balance = balance
        self.acc_status = acc_status
        self.uid = uid

        
class Transaction(db.Model):
    """This Class represent the transaction table in the database.
    
    Attributes:
    -----------
    id -> int, primary key
    balance -> int, not null
    receiver_acc -> str, not null, receiver account No.
    tran_type -> str, not null
    tran_date -> str, not null
    uid -> int, foreigtn key of users table 
    """
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key = True)
    balance = db.Column(db.Integer, nullable = False)
    receiver_ac = db.Column(db.String(30))
    account_no = db.Column(db.String(30), nullable = False)
    tran_type = db.Column(db.String(30), nullable = False)
    tran_date = db.Column(db.String(30), nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))


class Message(db.Model):
    """This Class represent the messages table in the database.
    
    Attributes:
    -----------
    id -> int, primary key
    name -> str, not null
    email -> str, not null
    message -> str, not null
    """
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(30), nullable = False)
    message = db.Column(db.String(255), nullable = False)

