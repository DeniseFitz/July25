from flask import Flask, render_template, url_for, flash, redirect # allow rendering of html code rather than printing it raw
from flask_wtf import FlaskForm
from flask_behind_proxy import FlaskBehindProxy ## add this line to imports
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
#import secrets
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

'''
Once you populate you can query the database from the terminal, 
notice "demo" is the name of my python file

python3
from demo import usertable
usertable.query.all()  # check the database
'''

app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app) 
app.config['SECRET_KEY'] = 'fb93246348ed383a9de5b7e77ff8d579' # be sure to use only the most recent key generated
#name of the database to create or use
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site2.db'

db = SQLAlchemy(app)

#Creates a table in the database named 'usertable"
class usertable(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"usertable('{self.username}', '{self.email}', '{self.password}')"
#new function to make sure table is created in the database when needed 
def __init__(self, username, email, password):
   self.username = username
   self.email = email
   self.password = password

#new code added to make sure table is created
db.create_all()

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_a = usertable(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user_a)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/")  
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page')

@app.route("/about")
def about():
    return render_template('about.html', subtitle='About Page')

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


if __name__ == '__main__':               # this should always be at the end avoids the need for environment variables
    app.run(debug=True, host="0.0.0.0")

#to run set environment variable:export FLASK_APP=demo unless you can use the command above
