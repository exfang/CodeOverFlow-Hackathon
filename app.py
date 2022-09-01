
from wtforms import Form, validators, StringField, IntegerField,SelectField, DateField, FileField, FloatField,FieldList, FormField, SubmitField
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from pythonFiles.customer_accounts import Login, Register, Email, OTP, ResetPassword, UpdateDetail, CurrentPassword
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from random import *
from Aboutusform import AboutusForm
from Aboutus import Aboutus
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import os
import pandas as pd
import json



app = Flask(__name__)
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'combatclimatechangetoday@gmail.com'
app.config['MAIL_PASSWORD'] = 'mspjwywbaehiyxtz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CC.db'
app.config['UPLOAD_FOLDER'] = 'static/IMAGE'
app.secret_key = 'any_random_string'

mail = Mail(app)
db = SQLAlchemy(app)


@app.before_request
def before_request():
    g.user = None
    if 'user id' in session:
        g.user = session['user id']


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

# Create Model
class Redeem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False, unique = True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    point_required = db.Column(db.Integer)
    itemImage = db.Column(db.String(200), nullable = False, unique = True)
    quantity_available = db.Column(db.Integer)
    redeemItem = db.relationship('RedeemedItem', backref = 'redeem', lazy = True)

    def __repr__(self) -> str:
        return 'Name %r' % self.name

class RedeemedItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    redeemItem_id = db.Column(db.Integer, db.ForeignKey('redeem.id') , nullable = False)

    def __repr__(self) -> str:
        return 'Name %r' % self.name

class Recycle(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    recycle_item = db.relationship('RecycledItem', backref = 'recycle_item', lazy = True)

class RecycledItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    material = db.Column(db.String(200), nullable = False)
    weight = db.Column(db.Float, nullable = False)
    recycle_id = db.Column(db.Integer, db.ForeignKey('recycle.id'))
    # add nullable to recycle_id

    def __init__(self, material, weight):
        self.material = material
        self.weight = weight

    @hybrid_property
    def calculate_points(self):
        if self.material == 'Paper':
            point = 2 * self.weight
        elif self.material == 'Plastic':
            point = 4 * self.weight
        else:
            point = 5 * self.weight
        return point

class air_pollution_SG(db.Model):
    id = db.Column('row_id', db.Integer, primary_key = True)
    Year = db.Column(db.String(4), nullable = False, unique = True)
    Sulphur_Dioxide = db.Column(db.Integer)  
    Nitrogen_Dioxide = db.Column(db.Integer)
    Particulate_Matter = db.Column(db.Integer)
    Carbon_Monoxide = db.Column(db.Integer)

    def __init__(self, *argv, **kwargs):
        if argv:
            self.Year = argv[0][0]
            self.Sulphur_Dioxide = argv[0][1]
            self.Nitrogen_Dioxide = argv[0][2]
            self.Particulate_Matter = argv[0][3]
            self.Carbon_Monoxide = argv[0][4]

# Create all intialised table / model
db.create_all()
# Read csv for data manuplination
df = pd.read_csv('M890641.csv')
keep = ['Data Series','Sulphur Dioxide (Maximum 24-Hour Mean) (Microgram Per Cubic Metre)','Nitrogen Dioxide (Annual Mean) (Microgram Per Cubic Metre)',
'Particulate Matter (PM10) (Annual Mean) (Microgram Per Cubic Metre)','Carbon Monoxide (Maximum 1-Hour Mean) (Milligram Per Cubic Metre)']
df = df.filter(items=keep)
df.rename(columns={
    'Data Series': 'Year', 
    'Sulphur Dioxide (Maximum 24-Hour Mean) (Microgram Per Cubic Metre)': 'Sulphur_Dioxide',
    'Nitrogen Dioxide (Annual Mean) (Microgram Per Cubic Metre)': 'Nitrogen_Dioxide',
    'Particulate Matter (PM10) (Annual Mean) (Microgram Per Cubic Metre)': 'Particulate_Matter',
    'Carbon Monoxide (Maximum 1-Hour Mean) (Milligram Per Cubic Metre)': 'Carbon_Monoxide',
    }, inplace=True)
df1 = df.values.tolist()
# Add into table
for data in df1:
    exitsted = air_pollution_SG.query.filter_by(Year = data[0]).first()
    if exitsted is None:
        db.session.add(air_pollution_SG(data))
        db.session.commit()
    else: 
        pass



def auto_create_staff():
    staff_check = Staffs.query.filter_by(email='john@gmail.com').first()
    if not staff_check:
        staff = Staffs(account_type='Staff', name='John', email='john@gmail.com')
        staff.set_password('staffpassw8rd')
        db.session.add(staff)
        db.session.commit()


# Create Form
class RedeemForm(Form):
    name = StringField('Item Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    point_required = IntegerField('Point Required', [validators.NumberRange(min=1, max=100000), validators.DataRequired()])
    quantity_available = IntegerField('Quantity Available', [validators.NumberRange(min=1, max=100000), validators.DataRequired()])
    itemImage = FileField('Image')



class RecycleItemForm(Form):
    material = SelectField('Recycle Material', [validators.DataRequired()], choices=[('Paper', 'Paper'), ('Plastic', 'Plastic'), ('Metal', 'Metal')])
    weight = FloatField('Weight (gram/g)', [validators.NumberRange(min=1, max=100000), validators.DataRequired()])

class RecycleForm(Form):
    items = FieldList(
        FormField(RecycleItemForm), min_entries=1
)


user_log = []


@app.route('/')
def home():
    auto_create_staff()
    if not user_log:
        session.clear()
        session['account_type'] = "Guest"
        
    result = db.session.query(
        air_pollution_SG.Year, 
        air_pollution_SG.Sulphur_Dioxide, 
        air_pollution_SG.Nitrogen_Dioxide,
        air_pollution_SG.Particulate_Matter,
        air_pollution_SG.Carbon_Monoxide).group_by(air_pollution_SG.Year).order_by(air_pollution_SG.Year).all()
    
    overall = db.session.query(
        db.func.sum(air_pollution_SG.Sulphur_Dioxide), 
        db.func.sum(air_pollution_SG.Nitrogen_Dioxide), 
        db.func.sum(air_pollution_SG.Particulate_Matter), 
        db.func.sum(air_pollution_SG.Carbon_Monoxide)).order_by(air_pollution_SG.Year).all()


    year_list = []
    sd_list = []
    nd_list = []
    pm_list = []
    cm_list = []
    for years, sd, nd, pm, cm in result:
        year = years.split('.')
        year_list.append(year[0])
        sd_list.append(sd)
        nd_list.append(nd)
        pm_list.append(pm)
        cm_list.append(cm)

    overall_list = []
    for sum_sd, sum_nd, sum_pm, sum_cm in overall:
        overall_list.append(sum_sd)
        overall_list.append(sum_nd)
        overall_list.append(sum_pm)
        overall_list.append(sum_cm)

    return render_template("home.html",
                            sulphur_dioxide = json.dumps(sd_list),
                            nitrogen_dioxide = json.dumps(nd_list),
                            particulate_matter = json.dumps(pm_list),
                            carbon_monoxide = json.dumps(cm_list),
                            dates_label =json.dumps(year_list),
                            overall = json.dumps(overall_list)
                        )


# Andrew - Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    log_in = Login(request.form)
    if request.method == 'POST' and log_in.validate():
        email = log_in.email.data
        password = log_in.password.data
        # Query the email's password
        user = Users.query.filter_by(email=email).first()
        staff = Staffs.query.filter_by(email=email).first()
        if user is not None:
            # Compare the hashed and non-hashed password
            check = check_password_hash(user.password, password)
            if check:
                log_in.email.data = ''
                log_in.password.data = ''
                session['account_type'] = user.account_type
                session['user id'] = user.id
                user_log.append('True')
                return redirect(url_for("account_detail"))
            else:
                flash("Wrong Password or Email address.")
        elif staff is not None:
            # Compare the hashed and non-hashed password
            check = check_password_hash(staff.password, password)
            if check:
                log_in.email.data = ''
                log_in.password.data = ''
                session['account_type'] = staff.account_type
                session['user id'] = staff.id
                user_log.append('True')
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
    if session['account_type'] != "Guest":
        if request.method == 'POST' and updateUser.validate():
            # user_detail stores the user's original data
            if session['account_type'] == 'Staff':
                user_detail = Staffs.query.filter_by(id=session['user id']).first()
            else:
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
            if session['account_type'] == 'Staff':
                user_detail = Staffs.query.filter_by(id=session['user id']).first()
            else:
                user_detail = Users.query.filter_by(id=session['user id']).first()
            updateUser.name.data = user_detail.name
            updateUser.email.data = user_detail.email
    else:
        return redirect(url_for('home'))
    return render_template("customer accounts/account_detail.html", form=updateUser)


# Andrew - Guest Forgot Password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    forgot_password = Email(request.form)
    email = forgot_password.email.data
    user_detail = Users.query.filter_by(email=email).first()
    staff_detail = Staffs.query.filter_by(email=email).first()
    if request.method == 'POST' and forgot_password.validate():
        if user_detail or staff_detail:
            session['reset_email'] = email
            if user_detail:
                session['user_type'] = 'User'
            else:
                session['user_type'] = 'Staff'
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
    if 'otp' not in session:
        return redirect(url_for('home'))
    otp_verification = OTP(request.form)
    if request.method == 'POST' and otp_verification.validate():
        if otp_verification.otp.data == session['otp']:
            session['authenticated'] = "Authentication successful."
            session.pop('otp')
            if 'delete_account' in session:
                session['delete_account'] = 'True'
                return redirect(url_for('confirm_deletion'))
            else:
                return redirect(url_for('reset_password'))
        else:
            flash("Wrong OTP code.")
    return render_template('customer accounts/forgot_password/otp_verification.html', form=otp_verification)


# Andrew - Guest reset password
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'authenticated' not in session:
        return redirect(url_for('home'))
    reset_password = ResetPassword(request.form)
    if request.method == 'POST' and reset_password.validate():
        if reset_password.new_password.data == reset_password.confirm_password.data:
            if session['user_type'] == 'User':
                user_detail = Users.query.filter_by(email=session['reset_email']).first()
            else:
                user_detail = Staffs.query.filter_by(email=session['reset_email']).first()
            user_detail.set_password(reset_password.new_password.data)
            db.session.commit()
            session['account_updated'] = "Account password has been updated successfully."
            session.pop('authenticated')
            session.pop('user_type')
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
    if session['account_type'] == "Guest":
        return redirect(url_for('home'))
    account_reset_password = CurrentPassword(request.form)
    password = account_reset_password.password.data
    if session['account_type'] == "User":
        user_detail = Users.query.filter_by(id=session['user id']).first()
    else:
        user_detail = Staffs.query.filter_by(id=session['user id']).first()
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
    if session['account_type'] == "Guest":
        return redirect(url_for('home'))
    delete_account = Email(request.form)
    if session['account_type'] == "User":
        user_detail = Users.query.filter_by(id=session['user id']).first()
    else:
        user_detail = Staffs.query.filter_by(id=session['user id']).first()
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


@app.route('/confirm_deletion')
def confirm_deletion():
    if session['account_type'] == "Guest" or 'delete_account' not in session:
        return redirect(url_for('home'))
    if session['account_type'] == "User":
        user_detail = Users.query.filter_by(id=session['user id']).first()
    else:
        user_detail = Staffs.query.filter_by(id=session['user id']).first()
    return render_template('customer accounts/delete_account/confirm_deletion.html', user=user_detail)


@app.route('/delete_account_confirmed')
def delete_account_confirmed():
    if session['account_type'] == "Guest" or 'delete_account' not in session:
        return redirect(url_for('home'))

    if session['account_type'] == "User":
        user_detail = Users.query.filter_by(id=session['user id']).first()
    else:
        user_detail = Staffs.query.filter_by(id=session['user id']).first()
    db.session.delete(user_detail)
    db.session.commit()
    session.clear()
    session['account_type'] = "Guest"
    session['account_updated'] = "Account has been successfully deleted."
    return redirect(url_for('login'))


@app.route('/delete_customer_accounts')
def delete_customer_accounts():
    if session['account_type'] == "Guest" or session['account_type'] == "User":
        return redirect(url_for('home'))

    users = Users.query.order_by(Users.id)
    staff = Staffs.query.order_by(Staffs.id)
    return render_template('staff/delete_accounts.html', users=users, staff=staff)


@app.route('/staff_delete_accounts/<int:id>', methods=['POST'])
def staff_delete_accounts(id):
    if session['account_type'] == "Guest" or session['account_type'] == "User":
        return redirect(url_for('home'))
    user_detail = Users.query.filter_by(id=id).first()
    session['account_deleted'] = user_detail.name + "'s account has been deleted successfully."
    db.session.delete(user_detail)
    db.session.commit()

    return redirect(url_for('delete_customer_accounts'))


@app.route('/logout')
def logout():
    session.clear()
    session['account_type'] = "Guest"
    return redirect(url_for('home'))


@app.route('/createRedeemItem', methods=['GET', 'POST'])
def create_redeem_item():
    form = RedeemForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'POST' and form.validate():
        posterFile = form.itemImage.data
        savePosterPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(posterFile.filename))
        posterFile.save(savePosterPath) # Save the file
 
        redeem = Redeem(name = form.name.data,
                        point_required = form.point_required.data, 
                        quantity_available = form.quantity_available.data, 
                        itemImage = form.itemImage.data.filename)
                        
        db.session.add(redeem)
        db.session.commit()
        flash("Item added Successfully")
        return redirect(url_for('redeem'))
    return render_template("createRedeemItem.html", form = form)

@app.route('/updateRedeemItem/<int:id>', methods=['GET', 'POST'])
def update_redeem_item(id):
    update_form = RedeemForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'POST' and update_form.validate():
        posterFile = update_form.itemImage.data
        savePosterPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(posterFile.filename))
        posterFile.save(savePosterPath) # Save the file

        our_items = Redeem.query.filter_by(id = id).first()
        our_items.name = update_form.name.data
        our_items.point_required = update_form.point_required.data
        our_items.quantity_available = update_form.quantity_available.data
        our_items.itemImage = update_form.itemImage.data.filename

        db.session.commit()
        return redirect(url_for('redeem'))
    else:
        our_items = Redeem.query.filter_by(id = id).first()
        update_form.name.data = our_items.name
        update_form.point_required.data = our_items.point_required
        update_form.quantity_available.data = our_items.quantity_available
        update_form.itemImage.data= our_items.itemImage

    return render_template("createRedeemItem.html", form = update_form)

@app.route('/deleteRedeem/<int:id>', methods=['GET', 'POST'])
def delete_redeem(id):
    our_items = Redeem.query.filter_by(id = id).first()
    try:
        db.session.delete(our_items)
        db.session.commit()
        flash('Item Deleted Successfully!!')

        return redirect(url_for('redeem'))
    except:
        flash('Whoops! There was a problem deleting item, try again.')


@app.route('/Redeem', methods=['GET', 'POST'])
def redeem():

    our_items = Redeem.query.order_by(Redeem.date_added)

    return render_template("redeem.html", our_items= our_items)


@app.route('/Add-Redeem/<int:id>', methods=['GET', 'POST'])
def add_redeem_item(id):
    item_redeemed = Redeem.query.filter_by(id = id).first()

    return render_template("redeemed.html", item_redeemed = item_redeemed)

@app.route('/process1', methods=['GET', 'POST'])
def process1():
    email_form = Email(request.form)
    if request.method == 'POST' and email_form.validate():
        user = Users.query.filter_by(email=email_form.email.data).first()
        if user:
            session['user id'] = user.id
            return redirect(url_for('process2'))
        else:
            flash("Email does not exist. Please ")
    return render_template("MachineProcess/process1.html", form=email_form)


@app.route('/process2', methods=['GET', 'POST'])
def process2():
    form = RecycleForm(request.form)
    if request.method == 'POST' and form.validate():
        recycle = Recycle()
        db.session.add(recycle)
        db.session.commit()
        for i in form.data['items']:
            recycle_item = RecycledItem(material = i['material'], weight = i['weight'])
            db.session.add(recycle_item)
            db.session.commit()
        return redirect(url_for('process3', id = recycle.id))
    return render_template("MachineProcess/process2.html", form = form)


@app.route('/process3/<int:id>', methods=['GET', 'POST'])
def process3(id):
    # recycled_items = RecycledItem.query.filter_by(id = id).first()
    recycled_items = RecycledItem.query.order_by(RecycledItem.recycle_id) # Can be Used for user history
    i = RecycledItem
    store_point = []
    for recycled_item in recycled_items:


        point = RecycledItem(recycled_item.material, recycled_item.weight)

        store_point.append(point.calculate_points)

    total_point = "{:.0f}".format(sum(store_point))


    return render_template("MachineProcess/process3.html", recycled_items = recycled_items, i = i, total_point = total_point)

if __name__ == "__main__":
    app.run(debug=True)
