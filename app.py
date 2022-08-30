from flask import Flask, render_template, request, redirect, url_for, session
from pythonFiles.customer_accounts import Login, Register, Email, OTP, ResetPassword
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'any_random_string'
app.config["MAIL_SERVER"] ='smtp.gmail.com'
app.config["MAIL_PORT"] =465
app.config["MAIL_USERNAME"] ='tackleclimatechanges@gmail.com'
app.config['MAIL_PASSWORD'] ='iaqeyqomxgwnstwi'
app.config['MAIL_USE_TLS'] =False
app.config['MAIL_USE_SSL'] =True


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    log_in = Login(request.form)
    if request.method == 'POST' and log_in.validate():
        pass
    return render_template("login and register/login.html", form=log_in)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register = Register(request.form)
    if request.method == 'POST' and register.validate():
        pass
    return render_template("login and register/register.html", form=register)


@app.route('/account_detail', methods=['GET', 'POST'])
def account_detail():
    updateUser = Email(request.form)
    if request.method == 'POST' and register.validate():
        pass
    return render_template("customer accounts/account_detail.html", form=updateUser)


@app.route('/redemption_history')
def redemption_history():

    return render_template('customer accounts/redemption_history.html')


@app.route('/recycle_history')
def recycle_history():

    return render_template('customer accounts/recycle_history.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    forgot_password = Email(request.form)
    return render_template('customer accounts/forgot_password/forgot_password.html', form=forgot_password)


@app.route('/otp_verification', methods=['GET', 'POST'])
def otp_verification():
    otp_verification = OTP(request.form)
    return render_template('customer accounts/forgot_password/otp_verification.html', form=otp_verification)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    reset_password = ResetPassword(request.form)
    return render_template('customer accounts/forgot_password/reset_password.html', form=reset_password)


if __name__ == "__main__":
    app.run(debug=True)
