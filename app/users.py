import email
from flask import Flask, render_template, redirect, request, session, flash
from app import app, db
from app.forms import RegisterationForm, LoginForm
from app.models import User, Account
from flask_login import login_user, logout_user, current_user, login_required



@app.route("/")
def homepage():
    return render_template("index.html")


# registeration page route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegisterationForm()
    form1 = LoginForm()
    if request.method == "GET":
        return render_template('register.html', form = form)
    else:
        form.validate()
        user = User(fullname=form.fullname.data, username=form.username.data,
                            email=form.email.data, password=form.password.data, 
                            gender=form.gender.data, phone=form.phone.data, 
                            birth_date=form.birth_date.data)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully fro {form.username.data}', category='success')
        return redirect('/login')


# Login page route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        if user and form.password.data == user.password:
           login_user(user)
           return redirect('/')
            
    return render_template("login.html", form=form)


@app.route('/withdraw')
@login_required
def withdraw():
    return "Withdraw page"


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

# profile settings
@app.route('/profile-settings/<uid>', methods=['GET', 'POST'])
def profile_settings(uid):
    form = RegisterationForm()
    user = User.query.filter_by(id=uid).first()
    form.fullname.data = user.fullname
    form.username.data = user.username
    form.email.data = user.email
    form.password.data = user.password
    form.phone.data = user.phone
    form.gender.data = user.gender
    form.role.data = user.role
    form.state.data = user.state
    return render_template('profile_settings.html', form=form, user=user)


# Edit user route
@app.route('/update-user/<uid>', methods=['GET', 'POST'])
def update_user(uid):
    if request.method == 'POST':
        form = RegisterationForm()
        record = User.query.filter_by(id=uid).first()
        record.fullname = form.fullname.data
        record.username = form.username.data
        record.email = form.email.data
        record.password = form.password.data
        record.phone = form.phone.data
        record.gender = form.gender.data
        record.role = form.role.data
        record.state = bool(form.state.data)
        db.session.commit()
        if current_user.role == 'admin' or current_user.role == 'sysuser':
            return redirect('/users')
        else:
            return redirect('profile')
    return render_template('index.html')


@app.route('/update-state/<uid>')
def update_state(uid):
    from random import randint
    user = User.query.get(uid)
    if user.state:
        user.state = not user.state
        db.session.commit()
        return redirect('/users')
    else:
        user.state = not user.state
        account = Account(account_no=str(user.id)+user.username, acc_status=True, uid=user.id)
        db.session.add(account)
        if db.session.commit():
            return "ok"
        
        return redirect('/users')

@app.route('/delete/<uid>')
def delete_user(uid):
    User.query.filter_by(id=uid).delete()
    db.session.commit()
    return redirect('/users')

# users list
@app.route('/users')
def user_list():
    users = User.query.all()
    return render_template('users_list.html',users=users)
        
        
def is_admin(uid):
    user = User.query.filter_by(id=uid).first()
    if user.role == 0:
        return True
    return False

def is_sys_user(uid):
    user = User.query.filter_by(id=uid).first()
    if user.role == 1:
        return True
    return False