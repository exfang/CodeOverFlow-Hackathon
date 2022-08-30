from wtforms import Form, StringField, PasswordField, validators, EmailField, DateField, IntegerField, DecimalField


class Login(Form):
    email = EmailField('Email', [validators.Length(min=5, max=150), validators.DataRequired(), validators.Email(message="Invalid Email")])
    password = PasswordField('Password', [validators.Length(min=8, max=150), validators.DataRequired()])


class Register(Form):
    email = EmailField('Email', [validators.Length(min=5, max=150), validators.DataRequired(), validators.Email(message="Invalid Email")])
    password = PasswordField('Password', [validators.Length(min=8, max=150), validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=8, max=150), validators.DataRequired()])


class Email(Form):
    email = EmailField('Email', [validators.Length(min=5, max=150), validators.DataRequired(), validators.Email(message="Invalid Email")])


class OTP(Form):
    otp = IntegerField('OTP‎ ‎ ‎ ‎ ‎ ', [validators.Length(min=6, max=6), validators.DataRequired()])


class ResetPassword(Form):
    new_password = PasswordField('New Password', [validators.Length(min=8, max=150), validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=8, max=150), validators.DataRequired()])
