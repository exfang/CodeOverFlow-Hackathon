import os
from flask import Flask, render_template, request, redirect, url_for, session
from Aboutusform import AboutusForm
from Aboutus import Aboutus

app = Flask(__name__)
app.secret_key = 'any_random_string'

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




if __name__ == "__main__":
    app.run(debug=True)