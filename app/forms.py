from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegisterationForm(FlaskForm):
    fullname = StringField(label="Full Name", validators=[DataRequired(), Length(max = 30)])
    username = StringField(label='Username', validators=[DataRequired(), Length(min = 3, max = 20)])
    account_no = StringField(label='Account No.', validators=[DataRequired(), Length(max = 30)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    birth_date = DateField(label='Date of Birth')
    gender = RadioField(choices=[('male','Male'), ('female','Female'), ('other', 'Other')])
    phone = StringField(label="Phone")
    password = PasswordField(label='Passsword', validators=[DataRequired(), Length(min = 8, max = 16),EqualTo('conffirm_password')])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired()])
    role = SelectField(label="Role", choices=(('sysuser','System User'), ('normal','Normal User')), validators=[DataRequired()])
    submit = SubmitField(label='Sign up')

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Passsword', validators=[DataRequired()])
    submit = SubmitField(label='Log in')

class ContactForm(FlaskForm):
    name = StringField(label='name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    subject = StringField(label="Subject", validators=[DataRequired()])
    message = StringField(label="Message", validators=[DataRequired(), Length(max = 200)])
    submit = SubmitField(label='Send Message')
    