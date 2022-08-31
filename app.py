import os
from Aboutusform import AboutusForm
from Aboutus import Aboutus

import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pythonFiles.customer_accounts import Login, Register, Email, OTP, ResetPassword, UpdateDetail, CurrentPassword
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from random import *


app = Flask(__name__)
app.secret_key = 'any_random_string'
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'tackleclimatechanges@gmail.com'
app.config['MAIL_PASSWORD'] = 'iaqeyqomxgwnstwi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CC.db'

mail=Mail(app)
db = SQLAlchemy(app)


# Andrew - User's database
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    points = db.Column(db.Integer(), nullable=True, unique=True)
    password = db.Column(db.String(), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Staffs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/Aboutus')
def create_contact():
    create_contact_form = AboutusForm(request.form)
    if request.method == 'POST' and create_contact_form.validate():
        contact_dict = {}
        db = SQLAlchemy.open('storage.db', 'c')

        try:
            contact_dict = db['Aboutus']
        except:
            print("Error in retrieving Users from storage.db.")

        contact = Aboutus.Aboutus(create_contact_form.name.data,
                               create_contact_form.email.data,
                               create_contact_form.remarks.data)

        contact_dict[contact.get_qn_id()] =contact
        db['Aboutus'] = contact_dict


        return redirect(url_for('home'))
    return render_template('Aboutus.html', form=create_contact_form)

@app.route('/Community')
def Community():
    return render_template("Community.html")

@app.route('/faq')
def faq():
    return render_template("FAQ.html")



# Andrew - Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    log_in = Login(request.form)
    if request.method == 'POST' and log_in.validate():
        email = log_in.email.data
        password = log_in.password.data
        # Query the email's password
        pw_to_check = Users.query.filter_by(email=email).first()
        if pw_to_check is not None:
            # Compare the hashed and non-hashed password
            check = check_password_hash(pw_to_check.password, password)
            if check:
                log_in.email.data = ''
                log_in.password.data = ''
                session['account_type'] = pw_to_check.account_type
                session['user id'] = pw_to_check.id
                return redirect(url_for("account_detail"))
            else:
                flash("Wrong Password or Email address.")
        else:
            flash("Wrong Password or Email address.")
    return render_template("login and register/login.html", form=log_in)


# Andrew - Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    register = Register(request.form)
    if request.method == 'POST' and register.validate():
        user = Users.query.filter_by(email=register.email.data).first()
        if register.password.data == register.confirm_password.data:
            if user is None:
                user = Users(account_type='User', name=register.name.data, email=register.email.data)
                user.set_password(register.password.data)
                db.session.add(user)
                db.session.commit()
            else:
                flash("Email exists already. Please ", 'emailexists')
                return render_template("login and register/register.html", form=register)
        else:
            flash("Confirm password not the same as password. Please try again.", 'wrongpassword')
            return render_template("login and register/register.html", form=register)
        register.email.data = ''
        register.password.data = ''
        session['account_updated'] = "Account Created Successfully!"
        return redirect(url_for("login"))
    return render_template("login and register/register.html", form=register)


# Andrew - User account detail
@app.route('/account_detail', methods=['GET', 'POST'])
def account_detail():
    updateUser = UpdateDetail(request.form)
    if 'account_type' in session:
        if request.method == 'POST' and updateUser.validate():
            # user_detail stores the user's original data
            user_detail = Users.query.filter_by(id=session['user id']).first()
            if updateUser.name.data != user_detail.name or updateUser.email.data != user_detail.email:
                # user_detail.email - set the original data email to
                # updateUser.email.data - the data the user entered (their new detail)
                user_detail.email = updateUser.email.data
                user_detail.name = updateUser.name.data
                try:
                    # commit the changes to the database (saving changes)
                    db.session.commit()
                    session['account_updated'] = "Account Details updated successfully!"
                    return render_template("customer accounts/account_detail.html", form=updateUser)
                except:
                    session['account_updated'] = "Unknown error occurred. Please try again."
            else:
                session['account_updated'] = "No changes made to the account details."
        else:
            user_detail = Users.query.filter_by(id=session['user id']).first()
            updateUser.name.data = user_detail.name
            updateUser.email.data = user_detail.email
    else:
        return redirect(url_for('home'))
    return render_template("customer accounts/account_detail.html", form=updateUser)


# Andrew - User redemption history
@app.route('/redemption_history')
def redemption_history():
    return render_template('customer accounts/redemption_history.html')


# Andrew - User recycle history
@app.route('/recycle_history', methods=['GET', 'POST'])
def recycle_history():
    users = Users.query.order_by(Users.id)
    return render_template('customer accounts/recycle_history.html', users=users)


# Andrew - Guest Forgot Password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    forgot_password = Email(request.form)
    email = forgot_password.email.data
    session['reset_email'] = email
    user_detail = Users.query.filter_by(email=email).first()
    if request.method == 'POST' and forgot_password.validate():
        if user_detail:
            otp = randint(100000, 999999)
            session['otp'] = otp
            msg = Message(subject="Climate Change Account Authentication", sender="tackleclimatechanges@gmail.com",
                          recipients=[email])
            msg.body = "Dear User, please use the code:"+str(otp)+" for your email authentication. Thank you."
            session['otp_verification'] = f'Code sent to {email}. Please enter the code for authentication.'
            mail.send(msg)
            return redirect(url_for('otp_verification'))
        else:
            flash("Email does not exist.")
    return render_template('customer accounts/forgot_password/forgot_password.html', form=forgot_password)


# Andrew - OTP Verification
@app.route('/otp_verification', methods=['GET', 'POST'])
def otp_verification():
    otp_verification = OTP(request.form)
    if request.method == 'POST' and otp_verification.validate():
        if otp_verification.otp.data == session['otp']:
            session['authenticated'] = "Authentication successful."
            if 'delete_account' in session:
                return redirect(url_for('confirm_deletion'))
            else:
                return redirect(url_for('reset_password'))
        else:
            flash("Wrong OTP code.")
    return render_template('customer accounts/forgot_password/otp_verification.html', form=otp_verification)


# Andrew - Guest reset password
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    reset_password = ResetPassword(request.form)
    if request.method == 'POST' and reset_password.validate():
        if reset_password.new_password.data == reset_password.confirm_password.data:
            user_detail = Users.query.filter_by(email=session['reset_email']).first()
            user_detail.set_password(reset_password.new_password.data)
            db.session.commit()
            session['account_updated'] = "Account password has been updated successfully."
            if 'account_reset_password' in session:
                return redirect(url_for('account_detail'))
            else:
                return redirect(url_for('login'))
        else:
            flash("Please ensure your new and confirm password is the same.")
    return render_template('customer accounts/forgot_password/reset_password.html', form=reset_password)


# Andrew - User's reset password
@app.route('/account_reset_password', methods=['GET', 'POST'])
def account_reset_password():
    account_reset_password = CurrentPassword(request.form)
    password = account_reset_password.password.data
    user_detail = Users.query.filter_by(id=session['user id']).first()
    email = user_detail.email
    if request.method == 'POST' and account_reset_password.validate():
        check = check_password_hash(user_detail.password, password)
        if check:
            otp = randint(100000, 999999)
            session['otp'] = otp
            msg = Message(subject="Climate Change Account Authentication", sender="tackleclimatechanges@gmail.com",
                          recipients=[email])
            msg.body = "Dear User, please use the code:"+str(otp)+" for your email authentication. Thank you."
            session['otp_verification'] = f'Code sent to {email}. Please enter the code for authentication.'
            mail.send(msg)
            session['account_reset_password'] = True
            session['reset_email'] = user_detail.email
            return redirect(url_for('otp_verification'))
        else:
            flash("Wrong Password.")
    return render_template('customer accounts/reset_password/current_password.html', form=account_reset_password)


# Andrew - User's reset password
@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    delete_account = Email(request.form)
    user_detail = Users.query.filter_by(id=session['user id']).first()
    email = user_detail.email
    if request.method == 'POST' and delete_account.validate():
        if delete_account.email.data == user_detail.email:
            otp = randint(100000, 999999)
            session['otp'] = otp
            msg = Message(subject="Climate Change Account Authentication", sender="tackleclimatechanges@gmail.com",
                          recipients=[email])
            msg.body = "Dear User, please use the code:"+str(otp)+" for your email authentication. Thank you."
            session['otp_verification'] = f'Code sent to {email}. Please enter the code for authentication.'
            mail.send(msg)
            session['delete_account'] = True
            session['reset_email'] = email
            return redirect(url_for('otp_verification'))
        else:
            flash("Wrong Email.")
    return render_template('customer accounts/delete_account/check_email.html', form=delete_account)


# @app.route('/confirm_deletion/<int:id>')
# def confirm_deletion():
#
#     return redirect(url_for('home'))


@app.route('/confirm_deletion')
def confirm_deletion():
    user = Users.query.filter_by(id=session['user id']).first()
    return render_template('customer accounts/delete_account/confirm_deletion.html', user=user)


@app.route('/delete_account_confirmed')
def delete_account_confirmed():
    user = Users.query.filter_by(id=session['user id']).first()
    db.session.delete(user)
    db.session.commit()
    session.clear()
    session['account_updated'] = "Account has been successfully deleted."
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
