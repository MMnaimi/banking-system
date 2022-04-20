from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegisterationForm(FlaskForm):
    fullname = StringField(label="Full Name", validators=[DataRequired(), Length(max = 30)])
    username = StringField(label='Username', validators=[DataRequired(), Length(min = 3, max = 20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    birth_date = DateField(label='Birthday')
    gender = RadioField(choices=[('male','Male'), ('female','Female'), ('other', 'Other')])
    phone = StringField(label="Phone")
    password = PasswordField(label='Passsword', validators=[DataRequired(), Length(min = 8, max = 16)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password', message="Enter the same password")])
    submit = SubmitField(label='Sign up')

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = StringField(label='Passsword', validators=[DataRequired()])
    submit = SubmitField(label='Log in')

class ContactForm(FlaskForm):
    name = StringField(label='name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    subject = StringField(label="Subject", validators=[DataRequired()])
    message = StringField(label="Message", validators=[DataRequired(), Length(max = 200)])
    submit = SubmitField(label='Send Message')
    