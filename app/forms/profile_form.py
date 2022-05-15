from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp


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


class ContactForm(FlaskForm):
    name = StringField(label='name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    subject = StringField(label="Subject", validators=[DataRequired()])
    message = StringField(label="Message", validators=[DataRequired(), Length(max = 200)])
    submit = SubmitField(label='Send Message')