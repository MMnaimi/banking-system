from flask import Flask, render_template, redirect, request, flash, url_for
from app import app, db, mail
from app.functions import for_normal_users, check_password, balance_validaty, log_transaction
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms.auth_form import RegisterationForm, LoginForm, ForgetForm, PasswordResetFrom
from app.forms.profile_form import UserProfileEditForm
from app.forms.transaction_forms import WithdrawForm, DepositForm, TransferForm
from app.models import User, Account, Message, Transaction
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from flask_mail import Message as Message2
from itsdangerous import BadTimeSignature, URLSafeTimedSerializer, SignatureExpired, BadSignature
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@app.route("/")
def homepage():
    """
        This function load home page.
    """
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    """
        This function load registeration form and register users.

    """
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = RegisterationForm()
    if request.method == "POST":
        user = User()
        check_data = user.custom_validation(form)
        if not form.validate():
            return render_template('register.html', form=form)
        if check_data.get('state'):
            user.create(fullname=form.fullname.data, username=form.username.data,
                            email=form.email.data, password=generate_password_hash(form.password.data), 
                            gender=form.gender.data, phone=form.phone.data, 
                            birth_date=form.birth_date.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created successfully for {form.username.data}', category='success',)
            return redirect(url_for('login'))
        else:
            flash(f"{check_data.get('message')}", category="error")


    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """
        This function load login page and login users to system.
        user can't login if their state is pending or deactive, this function return a message for them. 
    """

    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = LoginForm()
    args = request.args.to_dict(flat=False)
    default_route = '/'
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
            flash('Incorrect email or password', category='error')
            return redirect(url_for('login'))

        if user.state != 'active':
            flash('Please wait, Your account is not currently active', category='error')
            return redirect(url_for('login'))

        login_user(user)
        if args.get('redirect', ''):
            default_route = args.get('redirect')[0]
        return redirect(default_route)
       
    return render_template("login.html", form=form)

@app.route('/withdraw', methods=['GET', 'POST'])
@for_normal_users
def withdraw():
    """
        This function load the withdraw page for normal users only.
        withdraw money for normal users
    """
    account = Account.query.filter_by(uid = current_user.id).first()
    form = WithdrawForm()
    amount = form.amount.data
    error = False
    if request.method == 'POST':
        if not form.validate():
            return render_template('withdraw.html', form=form, account=account)
            
        if not check_password(form.password.data):
            flash(f"You have entered Incorrect password for user {current_user.username}, Please try agian!", category='error')
            error = True

        if not error and not balance_validaty(account, amount): 
            flash("You have insufficient balance", category='error')
            error = True

        if not error:
            account.balance -= abs(amount)
            log_transaction(amount=amount, tran_type='withdraw', account_no=account.account_no)
            db.session.commit()
            flash(f"you have successfully withdrew {form.amount.data}AF from your account")
            return redirect(url_for('withdraw'))
        

    return render_template('withdraw.html', form=form,account=account)

@app.route('/deposit', methods=['GET', 'POST'])
@for_normal_users
def deposit():
    """
        This function deposit money for normal users only.
    """

    account = Account.query.filter_by(uid = current_user.id).first()
    form = DepositForm()
    amount = form.amount.data
    if request.method == 'POST':

        if not form.validate():
            return render_template('deposit.html', form=form, account=account)

        if not check_password(form.password.data):
            flash(f'You have entered incorrect password for user {current_user.fullname}, Please try again!', category='error')
            return redirect(url_for('deposit'))

        account.balance += abs(amount)
        log_transaction(amount=amount, tran_type='deposit', account_no=account.account_no)
        db.session.commit()
        flash(f"{form.amount.data} AF added to your account", category='success')
        return redirect(url_for('deposit'))

    return render_template('deposit.html', form = form, account=account)

@app.route('/transfer', methods=['GET', 'POST'])
@for_normal_users
def transfer():
    """
        This function transfer money to another account.
    """
    default_redirect = 'transfer.html'
    sender  = Account.query.filter_by(uid = current_user.id).first()
    form = TransferForm()
    amount = form.amount.data
    error = False
    if request.method == 'POST':
        if not form.validate():
            return render_template('transfer.html', form=form, account=sender)
            
        receiver = Account.query.filter_by(account_no = form.account_no.data).first()

        if not check_password(form.password.data):
            flash(f"You have entered incorrect password for user {current_user.fullname}, Please try again!", category='error')
            error = True      

        if not error and not receiver or receiver.uid == sender.uid or not receiver.acc_status:   
            flash("The account number you have entered is wrong or not active", category="error")
            error = True

        if not error and not balance_validaty(sender, amount):
            flash("You have insufficient balance", category="error")
            error = True      

        if not error:
            receiver.balance += amount
            sender.balance -= amount
            log_transaction(amount=amount, receiver_ac=receiver.account_no, tran_type='transfer', account_no=sender.account_no)
            db.session.commit()
            flash("Transfer done successfully", category="success")
            return redirect(url_for('transfer'))

    return render_template(default_redirect, form=form, account=sender)

@app.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    """
        Logout user and redirect to homepage.
    """
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/user/profile-settings', methods=['GET'])
@login_required
def profile_settings():
    """
        This function load profile settings page.
    """
    form = UserProfileEditForm()
    user = User.query.filter_by(id=current_user.id).first()
    form.fullname.data = user.fullname
    form.username.data = user.username
    form.email.data = user.email
    form.phone.data = user.phone
    form.gender.data = user.gender
    form.birth_date.data = datetime.strptime(user.birth_date, '%Y-%m-%d')
    return render_template('user_profile_settings.html', form=form, user=user)

@app.route('/user/profile', methods=['GET'])
def profile():
    """
        This function load user profile page. 
    """
    if not current_user.is_authenticated:
        return render_template('404.html')

    user_record = db.session.query(User, User.id, User.username, User.fullname,User.email,User.gender, User.phone, 
                                User.birth_date, Account.account_no, Account.balance).join(Account, User.id == Account.uid,
                                isouter=True).filter(User.id == current_user.id).first()
    birth_date =datetime.strftime(datetime.strptime(user_record.birth_date, '%Y-%m-%d'), '%Y-%b-%d') 

    return render_template('profile.html', user = user_record, date = birth_date)
     
@app.route('/user/update-profile', methods=['GET', 'POST'])
@login_required
def update_user():
    """
        This function update user profile.
    """
    record = User.query.filter_by(id=current_user.id).first()
    if record.role !='admin':
        form = UserProfileEditForm()
        if request.method == 'POST':
            if form.validate():
                record.fullname = form.fullname.data
                record.username = form.username.data
                record.email = form.email.data
                record.phone = form.phone.data
                record.gender = form.gender.data
                record.birth_date = form.birth_date.data
                db.session.commit()
                flash('Profile updated successfully', category='success')
                return redirect(url_for('profile'))
            else:
             return render_template('user_profile_settings.html', form=form, user=record)

    return render_template('index.html')

@app.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('forget_password.html', form= form)
        email = form.email.data.lower()
        user = User.query.filter_by(email=email).first()
        if not user:
            return "Email Address Does not exists."
        token = serializer.dumps(email, salt='wallet')
        msg = Message2('Reset Password Link', sender='info@Wallet.com', recipients=[email])
        link =  url_for('reset_password', token=token, _external=True)
        msg.html = f'''<div class="grey-bg container pt-4">
            <div style = 'background: #f2f2f2; padding: 12px;'>
                <h4 style="text-align:center">Banking System</h4>
            </div>
            <hr>
            <div style="margin-top:30px; background: #fdfdfd; padding: 12px; border-radius: 8px;">
                 Hi <strong style="color:#00b08c;">{ user.fullname }</strong>,    
                <p class="pt-2">
                    Someone has requested a link to change your password. You can do this through the button below.
                </p>
                <div class="text-center">
                    <a href="{ link }">
                      <button style="padding:6px; cursor:pointer; ">Reset Password </button>
                    </a>
                </div>
                <hr style="margin-top:30px;">
                <p style="margin-top:30px">
                    If you did not request the reset password so please ignore this message.
                </p>
                <p>
                    Regards. <br>
                    <strong class="d-block">Banking System</strong>
                </p>
            </div>
        </div>'''
        mail.send(msg)
        flash("Email sent to your email address")
        return redirect(url_for('login'))

    return render_template('forget_password.html', form= form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = PasswordResetFrom()
    try:
        email = serializer.loads(token, salt='wallet', max_age=1800)
        user = User.query.filter_by(email=email).first()
        if request.method == 'POST':
            user.password = generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password changed successfully!')
            return redirect(url_for('login'))

    except SignatureExpired:
        return '<h2>The token is expired!</h2>'
    except BadTimeSignature:
        return '<h2> Invalid token or token expired'
    except BadSignature:
        return '<h2> Invalid token or token expired'

    return render_template('reset_password.html', form = form)

@app.route('/message', methods=['GET', 'POST'])
def send_message():
    """
        This function store contact messages. 
        any one can send message to system not only registered users.
    """
    if request.method == 'POST':
        message = Message(name = request.form['name'], email = request.form['email'], message = request.form['message'])
        db.session.add(message)
        db.session.commit()
        flash("Your message has been sent. Thank you!")
        return redirect('/#contact')
    return render_template('404.html')

@app.route('/user/log', methods=['GET', 'POST'])
@login_required
@for_normal_users
def user_log():
    log = Transaction.query.filter(Transaction.uid == current_user.id).all()
    return render_template('logs.html', logs = log)