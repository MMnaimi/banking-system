from flask import Flask, render_template, redirect, request, flash, url_for
from app import app, db
from app.functions import is_admin, is_sys_user
from app.forms.profile_form import AdminProfileEditForm
from app.models import User, Account, Transaction
from flask_login import current_user, login_required
from datetime import datetime

@app.route('/admin/user-settings/<uid>', methods=['GET', 'POST'])
def admin_users_settings(uid):
    """ 
        This function  load user settings page for admin and system users.

        parameter:
        uid: The id of users, we want to change their profile.
    """
    user = User.query.get(uid)
    if current_user.role == 'normal':
        return  render_template('404.html')

    form = AdminProfileEditForm()
    form.fullname.data = user.fullname
    form.username.data = user.username
    form.email.data = user.email
    form.phone.data = user.phone
    form.gender.data = user.gender
    form.birth_date.data = datetime.strptime(user.birth_date, '%Y-%m-%d')
    form.role.data   = user.role
    form.uid.data = uid
    return render_template('admin_users_settings.html', form=form, user=user)

@app.route('/admin/update-user/', methods=['GET', 'POST'])
@login_required
def admin_user_update():
    """
        This function update the users profile. 
        Admin and system users have access to this function
    """

    if current_user.role == 'normal':
        return redirect(url_for('homepage'))
        
    form = AdminProfileEditForm()
    record = User.query.filter_by(id=form.uid.data).first()

    if record.role =='admin':
        flash("Only admin can change admin settings")
        return redirect(url_for('user_list'))

    if request.method == 'POST':
        if form.validate():
            record.fullname = form.fullname.data
            record.username = form.username.data
            record.email = form.email.data
            record.phone = form.phone.data
            record.gender = form.gender.data
            if current_user.role == 'admin':
                record.role = form.role.data
            else:
                record.role = record.role
            db.session.commit()
            flash('User updated successfully!')
            return redirect(url_for('user_list'))
        else:
            return render_template('admin_users_settings.html', form=form, user=record)
        
    return redirect(url_for('homepage'))

@app.route('/update-state/<uid>')
def update_state(uid):

    """
        This function update the state of users from pending to active, from active to deactive and vice versa.

        parameter:
        uid: id of user want to change their state.
    """

    if current_user.is_authenticated and (is_admin(current_user.id) or is_sys_user(current_user.id)):
        from random import randint
        user = User.query.get(uid)
        if user.id == current_user.id:
            flash("Yun can't change your state", category="error")
            return redirect(url_for('user_list'))
        if user.state == 'active':
            user.state = 'deactive'
            account = Account.query.filter_by(uid = user.id).first()
            account.acc_status = False
            db.session.commit()
            return redirect(url_for('user_list'))
        elif user.state == 'deactive':
            user.state = 'active'
            account = Account.query.filter_by(uid = user.id).first()
            account.acc_status = True
            db.session.commit()
            return redirect(url_for('user_list'))

        user.state = 'active'
        account = Account(account_no=randint(13**(13-1), (13**13)-1), acc_status=True, uid=user.id)
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('user_list'))
    else:
        flash("Authorization denied", category='error')
        return render_template('404.html'), 404

@app.route('/delete/<uid>')
def delete_user(uid):
    """
       This function Delete the user with id = uid.
       Only admin and system user can delete normal users

        parameter
        uid: id of user we are going to delete.
    """

    if current_user.role == "admin" or current_user.role == 'sysuser':
        user =  User.query.filter_by(id=uid).first()
        if user.role != 'admin' and current_user.id != user.id:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully', category='success')
            return redirect(url_for('user_list'))
        else:
            flash("You can't delete this account", category="error")
            return redirect(url_for('user_list'))

@app.route('/users', methods=['GET', 'POST'])
@login_required
def user_list():
    """
        This function return list of all users for admin and system users.
        Only admin and system user can see users list
    """

    if current_user.role == 'admin' or current_user.role == 'sysuser':
        users = db.session.query(User, User.id, User.username, User.fullname,User.email,User.gender, User.phone,
                                    User.birth_date, User.state, User.role, Account.account_no,
                                    Account.balance).join(Account, User.id == Account.uid, isouter=True).all()

        return render_template('users_list.html',users=users)

    else:
        return render_template('index.html')

@app.route('/log', methods=['get', 'POST'])
@login_required
def logs():
    if current_user.role == 'normal':
        return redirect(url_for('homepage'))
    logs = db.session.query(Transaction, User.username, User.fullname,User.email,User.gender, User.phone,
                                    User.birth_date, User.state, User.role,Transaction.id, Transaction.account_no,
                                    Transaction.balance, Transaction.receiver_ac, Transaction.tran_type, Transaction.tran_date).join(User, User.id == Transaction.uid, isouter=True).all()
    return render_template('logs.html', logs = logs)