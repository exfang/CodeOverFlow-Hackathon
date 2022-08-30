from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'any_random_string'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/redeem')
def redeem():
    return render_template("redeem.html")

if __name__ == "__main__":
    app.run(debug=True)