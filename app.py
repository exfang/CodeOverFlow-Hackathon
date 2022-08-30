from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.secret_key = 'any_random_string'
#Initialize The Database
db = SQLAlchemy(app)

# Create Model
class Redeem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False, unique = True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    point_required = db.Column(db.Integer)
    filename = db.Column(db.String(200), nullable = False, unique = True)
    quantity_available = db.Column(db.Integer)

    def __repr__(self) -> str:
        return 'Name %r' % self.name

class RedeemForm(FlaskForm):
    name = StringField('Item Name', validators = [DataRequired()])
    point_required = IntegerField('Point Required', validators = [DataRequired()])
    quantity_available = IntegerField('Quantity Available', validators = [DataRequired()])
    filename = FileField('Image', validators = [DataRequired()])
    submit = SubmitField('Submit', validators = [DataRequired()])


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/createRedeemItem', methods=['POST'])
def create_redeem_item():
    form = RedeemForm()
    if form.validate_on_submit():
        redeem = Redeem.query.filter_by(form.name.data).first()
        print(redeem)
        db.session.add(redeem)
        db.session.commit()
        flash("Item added Successfully")
        return redirect(url_for('redeem'))
    return render_template("createRedeemItem.html", form = form)

@app.route('/Redeem', methods=['GET', 'POST'])
def redeem():
    our_items = []
    our_items = Redeem.query.order_by(Redeem.date_added)

    return render_template("redeem.html", our_items= our_items)

@app.route('/process1', methods=['GET', 'POST'])
def process1():

    return render_template("MachineProcess/process1.html")



@app.route('/process2', methods=['GET', 'POST'])
def process2():

    return render_template("MachineProcess/process2.html")



@app.route('/process3', methods=['GET', 'POST'])
def process3():

    return render_template("MachineProcess/process3.html")

if __name__ == "__main__":
    app.run(debug=True)