import email
from flask import Flask, render_template, redirect, request, url_for, flash
from app import app, db
from app.forms import RegisterationForm, LoginForm
from app.models import User


@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User(fullname=form.fullname.data, username=form.username.data,
                    email=form.email.data, password=form.password.data, 
                    gender=form.gender.data, phone=form.phone.data, 
                    birth_date=form.birth_date)
        print("user")
        db.session(user)
        db.session.commit()
        return 'Registered successfully'
    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first
        if form.email.data == user.email and form.password.data == user.password:
            print('You logged in successfully!!!!!!')
    return render_template("login.html", form=form)

