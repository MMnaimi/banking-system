from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, PasswordField, DateField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp, NumberRange, ValidationError


class RegisterationForm(FlaskForm):
    fullname = StringField(label="Full Name", validators=[DataRequired(), Length(max = 30)])
    username = StringField(label='Username', validators=[DataRequired(), Length(min = 5, max = 20), Regexp('^[a-zA-Z0-9_-]+$',message="Username must contain only letters, number, underscore or hyphen")])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    birth_date = DateField(label='Date of Birth')
    gender = RadioField(choices=[('male','Male'), ('female','Female'), ('other', 'Other')])
    phone = StringField(label="Phone")
    password = PasswordField(label='Passsword', validators=[Length(min = 8, max = 16), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[Length(min = 8, max = 16), DataRequired(), EqualTo('password')])
    state = SelectField(label="State",choices=((True,'Active'), (False,'Pending')), default=(False) ,validators=[DataRequired()])
    role = SelectField(label="Role", choices=(('sysuser','System User'), ('normal','Normal User')), default=('normal'), validators=[DataRequired()])
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


class WithdrawForm(FlaskForm):
    amount = IntegerField(label='Amount', render_kw={'placeholder':'Amount of money...', 'class':'form-control'}, validators=[DataRequired(), NumberRange(min=500, max=20000, message="Amount must be between 500 and 20000")])
    password = PasswordField(label='Password', render_kw={'placeholder':'Password...', 'class':'form-control'}, validators=[DataRequired()])
    submit = SubmitField(label='Done')


class DepositForm(FlaskForm):
    amount = IntegerField(label='Amount', render_kw={'placeholder':'Amount of money...', 'class':'form-control'}, validators=[DataRequired(), NumberRange(min=500, max=1000000, message="Amount must be between 500 and 1000000")])
    password = PasswordField(label='Password', render_kw={'placeholder':'Password...', 'class':'form-control'}, validators=[DataRequired()])
    submit = SubmitField(label='Done')


class TransferForm(FlaskForm):
    account_no = StringField(label='Account number',render_kw={'placeholder':'Account No.', 'class':'form-control'}, validators=[DataRequired()])
    amount = IntegerField(label='Amount', render_kw={'placeholder':'Amount of money...', 'class':'form-control'}, validators=[DataRequired(), NumberRange(min=500, max=20000, message="Amount must be between 500 and 20000")])
    password = PasswordField(label='Password', render_kw={'placeholder':'Password...', 'class':'form-control'}, validators=[DataRequired()])
    submit = SubmitField(label='Done')


class PasswordResetForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label = 'Reset Password')


class AdminProfileEditForm(FlaskForm):
    fullname = StringField(label="Full Name", validators=[DataRequired(), Length(min = 5, max = 30)])
    username = StringField(label='Username', validators=[DataRequired(), Length(min = 5, max = 20), Regexp('^[a-zA-Z0-9_-]+$', message="Username must contain only letters, numbers or underscore")])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    birth_date = DateField(label='Date of Birth')
    phone = StringField(label="Phone")
    gender = RadioField(choices=[('male','Male'), ('female','Female'), ('other', 'Other')])
    role = SelectField(label="Role", choices=(('sysuser','System User'), ('normal','Normal User')), validators=[DataRequired()])
    uid = HiddenField()
    submit = SubmitField(label='Save Profile')


class UserProfileEditForm(FlaskForm):
    fullname = StringField(label="Full Name", validators=[DataRequired(), Length(max = 30)])
    username = StringField(label='Username', validators=[DataRequired(), Length(min = 5, max = 20), Regexp('^[a-zA-Z0-9_-]+$', message="Username must contain only letters, numbers or underscore")])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    phone = StringField(label="Phone")
    gender = RadioField(choices=[('male','Male'), ('female','Female'), ('other', 'Other')])
    birth_date = DateField(label='Date of Birth')
    submit = SubmitField(label='Save Profile')

