from cProfile import label
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp


class RegisterationForm(FlaskForm):
    fullname = StringField(label="Full Name", render_kw={'placeholder':'Enter Fullname'}, validators=[DataRequired(), Length(max = 30)])
    username = StringField(label='Username', render_kw={'placeholder':'Enter Username'}, validators=[DataRequired(), Length(min = 5, max = 20), Regexp('^[a-zA-Z0-9_-]+$',message="Username must contain only letters, number, underscore or hyphen")])
    email = StringField(label='Email', render_kw={'placeholder':'Enter Email'}, validators=[DataRequired(), Email()])
    birth_date = DateField(label='Date of Birth')
    gender = RadioField(choices=[('male','Male'), ('female','Female'), ('other', 'Other')])
    phone = StringField(label="Phone",render_kw={'placeholder':'Enter phone number'} )
    password = PasswordField(label='Passsword', render_kw={'placeholder':'Enter password'}, validators=[Length(min = 8, max = 16), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', render_kw={'placeholder':'Confirm Password'}, validators=[Length(min = 8, max = 16), DataRequired(), EqualTo('password')])
    state = SelectField(label="State",choices=((True,'Active'), (False,'Pending')), default=(False) ,validators=[DataRequired()])
    role = SelectField(label="Role", choices=(('sysuser','System User'), ('normal','Normal User')), default=('normal'), validators=[DataRequired()])
    submit = SubmitField(label='Sign up')


class LoginForm(FlaskForm):
    email = StringField(label='Email', render_kw={'placeholder':'Enter Email'}, validators=[DataRequired(), Email()])
    password = PasswordField(label='Passsword', render_kw={'placeholder':'Enter Password'}, validators=[DataRequired()])
    submit = SubmitField(label='Log in')


class ForgetForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label = 'Reset Password')

class PasswordResetFrom(FlaskForm):
    current_password = PasswordField(label='Current Password', validators=[DataRequired()])