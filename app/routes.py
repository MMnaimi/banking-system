import email
from flask import Flask, render_template, redirect, request, url_for, flash
from app import app, db
from app.forms import RegisterationForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterationForm()
    if request.method == "POST":
        user = User(fullname=form.fullname.data, username=form.username.data,
                        email=form.email.data, password=form.password.data, 
                        gender=form.gender.data, phone=form.phone.data, 
                        birth_date=form.birth_date.data)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully fro {form.username.data}', category='success')
        return redirect(url_for('app.login'))
        
    return render_template("register.html", form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('index.html')
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        if user and form.password.data == user.password:
           login_user(user)
           return render_template('index.html')
            
    return render_template("login.html", form=form)


@app.route('/withdraw')
@login_required
def withdraw():
    return "Withdraw page"


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')