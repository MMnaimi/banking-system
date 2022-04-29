from flask import Flask, render_template, redirect, request, flash
from app import app, db
from app.forms import RegisterationForm, LoginForm, TransactionForm
from app.models import User, Account
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime



def is_admin(uid):
    user = User.query.filter_by(id=uid).first()
    if user.role == 'admin':
        return True
    return False

def is_sys_user(uid):
    user = User.query.filter_by(id=uid).first()
    if user.role == 'sysuser':
        return True
    return False

def transaction_auth():
    pass



@app.route("/")
def homepage():
    return render_template("index.html")


# registeration page route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect("/")

    form = RegisterationForm()
    if request.method == "POST":
        form.validate()
        user = User(fullname=form.fullname.data, username=form.username.data,
                            email=form.email.data, password=form.password.data, 
                            gender=form.gender.data, phone=form.phone.data, 
                            birth_date=form.birth_date.data)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {form.username.data}', category='success',)
        return redirect('/login')

    return render_template("register.html", form = form)


# Login page route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    args = request.args.to_dict(flat=False)
    default_route = '/'
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        if not user and form.password.data != user.password:
            flash('Incorrect email or password')
            return redirect('/login')

        if user.state != 'active':
            flash('Please wait, Your account is not currently active')
            return redirect('/login')

        login_user(user)
        if args.get('redirect', ''):
            default_route = args.get('redirect')[0]
        return redirect(default_route)
       
    return render_template("login.html", form=form)


@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if not (current_user.is_authenticated and current_user.state == 'active' and not(is_admin(current_user.id) or is_sys_user(current_user.id))):
        flash(f"You need to log in first", category='error')
        return redirect('/login')

    account = Account.query.filter_by(uid = current_user.id).first()
    form = TransactionForm()
    amount = form.amount.data
    if request.method == 'POST':

        if current_user.password != form.password.data:
            flash(f"You have entered Incorrect password for user {current_user.username}, Please try agian!")
            return redirect('/withdraw')

        if account.balance - 500 <= amount: 
            flash("You have insufficient balance", category='error')
            return redirect('/withdraw')

        account.balance -= abs(amount)
        db.session.commit()
        flash(f"you have successfully withdrew {form.amount.data}AF from your account")
        return redirect ('/withdraw')

    return render_template('withdraw.html', form=form,balance=account.balance)



@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if not (current_user.is_authenticated and current_user.state == 'active' and not(is_admin(current_user.id) or is_sys_user(current_user.id))):
        flash(f"log in to your account first", category='error')
        return redirect('/login?redirect=/deposit')

    account = Account.query.filter_by(uid = current_user.id).first()
    form = TransactionForm()
    amount = form.amount.data
    if request.method == 'POST':

        if current_user.password != form.password.data:
            flash(f'You have entered incorrect password for user {current_user.fullname}, Please try again!')
            return redirect('/deposit')

        account.balance += abs(amount)
        db.session.commit()
        flash(f"{form.amount.data} AF added to your account", category='success')

    return render_template('deposit.html', form = form, balance=account.balance)



@app.route('/transfer', methods=['GET', 'POST'])
def transfer():

    if not (current_user.is_authenticated and current_user.state == 'active' and not(is_admin(current_user.id) or is_sys_user(current_user.id))):
        flash(f"log in to your account first", category='error')
        return redirect('/login')

    default_redirect = '/transfer'
    sender  = Account.query.filter_by(uid = current_user.id).first()
    form = TransactionForm()
    amount = form.amount.data
    if request.method == 'POST':
        reciever = Account.query.filter_by(account_no = form.account_no.data).first()
        
        if current_user.password != form.password.data:
            flash(f"You have entered incorrect password for user {current_user.fullname}, Please try again!")
            return redirect(default_redirect)

        if not reciever or reciever.uid == sender.uid:   
            flash("You have entered incorrect account number", category="error")
            return redirect(default_redirect)

        if sender.balance - 500 <= amount:
            flash("You have insufficient balance", category="error")
            return redirect(default_redirect)

        reciever.balance += amount
        sender.balance -= amount
        db.session.commit()
        flash("Transfer done successfully", category="success")
        return redirect(default_redirect)                 
    return render_template("transfer.html", form=form, balance=sender.balance)



@app.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')



# user profile settings
@app.route('/user/profile-settings', methods=['GET', 'POST'])
@login_required
def profile_settings():
    form = RegisterationForm()
    user = User.query.filter_by(id=current_user.id).first()
    form.fullname.data = user.fullname
    form.username.data = user.username
    form.email.data = user.email
    form.phone.data = user.phone
    form.gender.data = user.gender
    form.birth_date.data = datetime.strptime(user.birth_date, '%Y-%m-%d')
    return render_template('user_profile_settings.html', form=form, user=user)

# admin profile settings
@app.route('/admin/user-settings/<uid>', methods=['GET', 'POST'])
@login_required
def admin_users_settings(uid):
    user = User.query.get(uid)
    if current_user.role != 'admin' or current_user.role != 'sysuser':
        return  render_template('404.html')

    form = RegisterationForm()
    form.fullname.data = user.fullname
    form.username.data = user.username
    form.email.data = user.email
    form.phone.data = user.phone
    form.gender.data = user.gender
    form.birth_date.data = datetime.strptime(user.birth_date, '%Y-%m-%d')
    form.role.data   = user.role
    form.uid.data = uid
    return render_template('admin_users_settings.html', form=form, user=user)

    



@app.route('/user/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return render_template('404.html')

    user_record = db.session.query(User, User.id, User.username, User.fullname,User.email,User.gender, User.phone, \
                                User.birth_date, Account.account_no, Account.balance).join(Account, User.id == Account.uid, isouter=True).filter(User.id == current_user.id).first()
    return render_template('profile.html', user = user_record)

        




# Edit user route
@app.route('/user/update-profile', methods=['GET', 'POST'])
@login_required
def update_user():
    record = User.query.filter_by(id=current_user.id).first()
    if record.role !='admin':
        if request.method == 'POST':
            form = RegisterationForm()
            record.fullname = form.fullname.data
            record.username = form.username.data
            record.email = form.email.data
            record.phone = form.phone.data
            record.gender = form.gender.data
            record.birth_date = form.birth_date.data
            db.session.commit()
            return redirect('/user/profile')

    return render_template('index.html')


# Admin edit user route
@app.route('/admin/update-user/', methods=['GET', 'POST'])
@login_required
def admin_user_update():
    if current_user.role not in ('admin', 'sysuser'):
        return redirect('/')
        
    form = RegisterationForm()
    record = User.query.filter_by(id=form.uid.data).first()

    if record.role =='admin':
        flash("Only admin can change admin settings")
        return redirect('/users')

    if request.method == 'POST':
        record.fullname = form.fullname.data
        record.username = form.username.data
        record.email = form.email.data
        record.password = record.password
        record.phone = form.phone.data
        record.gender = form.gender.data
        if current_user.role == 'admin':
            record.role = form.role.data
        else:
            record.roel = record.role
        db.session.commit()
        return redirect('/users')
        
    return render_template('index.html')




@app.route('/update-state/<uid>')
def update_state(uid):
    if current_user.is_authenticated and (is_admin(current_user.id) or is_sys_user(current_user.id)):
        from random import randint
        user = User.query.get(uid)
        if user.state == 'active':
            user.state = 'deactive'
            account = Account.query.filter_by(uid = user.id).first()
            account.acc_status = False
            db.session.commit()
            return redirect('/users')
        elif user.state == 'deactive':
            user.state = 'active'
            account = Account.query.filter_by(uid = user.id).first()
            account.acc_status = True
            db.session.commit()
            return redirect('/users')
        else:
            user.state = 'active'
            account = Account(account_no=str(user.id)+str(randint(100, 1000))+user.username, acc_status=True, uid=user.id)
            db.session.add(account)
            db.session.commit()
            return redirect('/users')
    else:
        flash("Authorization denied", category='error')
        return render_template('404.html'), 404



@app.route('/delete/<uid>')
def delete_user(uid):
    if current_user.role == "admin" or current_user.role == 'sysuser':
        user =  User.query.filter_by(id=uid).first()
        if user.role != 'admin':
            user.delete()
            db.session.commit()
            flash('User deleted successfully', category='success')
            return redirect('/users')
        else:
            flash("Admin can not be deleted")
            return redirect('/users')



# users list
@app.route('/users', methods=['GET', 'POST'])
def user_list():
    if current_user.role == 'admin' or current_user.role == 'sysuser':
        users = db.session.query(User, User.id, User.username, User.fullname,User.email,User.gender, User.phone, \
                                    User.birth_date, User.state, User.role, Account.account_no, Account.balance).join(Account, User.id == Account.uid, isouter=True).all()

        return render_template('users_list.html',users=users)
    else:
        return render_template('404.html')
        
        


        
