from functools import wraps
from xml.dom import ValidationErr
from flask import Flask, render_template
from app import db
from werkzeug.security import  check_password_hash
from app.models import User, Transaction
from flask_login import current_user
from datetime import datetime

def for_normal_users(func):
    """
        This function decorate transaction route functions to varify that the user is logged in, user is not a system user or an admin.
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.state == 'active' and not(is_admin(current_user.id) or is_sys_user(current_user.id))):
            return render_template('404.html')
        return func(*args, **kwargs)
    return wrap

def check_password(password):
    """
        This function check correctness of password against current user password stored in db.

        Return -> boolean

        parameter
        ---------
        password -> password entered by users
    """
    if not check_password_hash(current_user.password, password):
        return False
    return True
    
def balance_validaty(sender, amount):
    """
        This function validate sufficiency of the account for transactions.

        Return: Boolean

        parameter
        ---------
        sender -> who does the transaction
        amount -> amount of money use in transaction
    """
    if sender.balance - 500 <= amount:
        return False
    return True

def log_transaction(**kwrgs):
    """
        This function store transactions

        parameter
        ---------
        balance -> amount of money 
        receiver_ac -> if the transactions is transfer we need to store receiver account number
        tran_type -> type of the transaction possible value -> transfer, withdraw, deposit
        tran_date -> when the transaction is done
        uid -> who did the transaction
        account_no -> user account number who did the transaction 
    """
    log = Transaction(
        balance = kwrgs.get('amount'), 
        receiver_ac = kwrgs.get('receiver_ac'), 
        tran_type = kwrgs.get('tran_type'),  
        tran_date = datetime.now().strftime("%b-%d-%Y %H:%M %p"), 
        uid = current_user.id, 
        account_no = kwrgs.get('account_no')
        )
    db.session.add(log)
    
def is_admin(uid):
    """ This function show user is admin or not.
    
    Return: boolean
    True for admin
    False for none admin

    """
    user = User.query.filter_by(id=uid).first()
    if user.role == 'admin':
        return True
    return False

def is_sys_user(uid):
    """ This function show the user is system user or not

    Return: boolean
    True for system users
    False for none system users
    """
    user = User.query.filter_by(id=uid).first()
    if user.role == 'sysuser':
        return True
    return False
