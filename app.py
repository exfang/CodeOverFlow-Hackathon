from email.policy import default
from tkinter.tix import Select
from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import Form, validators, StringField, IntegerField,SelectField, DateField, FileField, FloatField,FieldList, FormField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import os

app = Flask(__name__)
#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['UPLOAD_FOLDER'] = 'static/IMAGE'
app.secret_key = 'any_random_string'
#Initialize The Database
db = SQLAlchemy(app)

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



@app.route('/')
def home():
    return render_template("home.html")

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

    return render_template("MachineProcess/process1.html")



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