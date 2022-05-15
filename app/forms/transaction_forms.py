from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class WithdrawForm(FlaskForm):
    amount = IntegerField(label='Amount To Withdraw (min 500 - max 20,000)', render_kw={'placeholder':'0.0', 'class':'form-control'}, validators=[DataRequired(), NumberRange(min=500, max=20000, message="Amount must be between 500 and 20000")])
    password = PasswordField(label='Password', render_kw={'placeholder':'Password', 'class':'form-control'}, validators=[DataRequired()])
    submit = SubmitField(label='Done')


class DepositForm(FlaskForm):
    amount = IntegerField(label='Amount To Deposit (min 500 - max 1,000,000)', render_kw={'placeholder':'0.0', 'class':'form-control'}, validators=[DataRequired(), NumberRange(min=500, max=1000000, message="Amount must be between 500 and 1000000")])
    password = PasswordField(label='Password', render_kw={'placeholder':'Password', 'class':'form-control'}, validators=[DataRequired()])
    submit = SubmitField(label='Done')


class TransferForm(FlaskForm):
    account_no = StringField(label='Transfer To',render_kw={'placeholder':'Account No.', 'class':'form-control'}, validators=[DataRequired()])
    amount = IntegerField(label='Amount To Transfer (min 500 - max 20,000)', render_kw={'placeholder':'0.0', 'class':'form-control'}, validators=[DataRequired(), NumberRange(min=500, max=20000, message="Amount must be between 500 and 20000")])
    password = PasswordField(label='Password', render_kw={'placeholder':'Password', 'class':'form-control'}, validators=[DataRequired()])
    submit = SubmitField(label='Done')
