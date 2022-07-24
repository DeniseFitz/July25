from flask import Flask, render_template, url_for, flash, redirect, request # allow rendering of html code rather than printing it raw
#from flask import Markup
#flash(Markup('Please sign in <a href='/'))
from flask_behind_proxy import FlaskBehindProxy  
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean

'''
https://flask.palletsprojects.com/en/2.1.x/patterns/wtforms/ good info

Once you populate you can query the database from the terminal, 
notice "demo" is the name of my python file, User is the class name and the table name is usertable

python3
from demo import User  
User.query.all()  
from demo import logintable
logintable.query.column_descriptions
'''

app = Flask(__name__)         #gets the name of this .py file so Flask knows it's name
proxied = FlaskBehindProxy(app) 
app.config['SECRET_KEY'] = 'fb93246348ed383a9de5b7e77ff8d579' # be sure to use only the most recent key generated
#name of the database to create or use
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site2.db'

db = SQLAlchemy(app)

#Because of __tablename__ database table is 'usertable"
class User(db.Model):
  __tablename__ = 'usertable' #if do not specify the table name is user
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"usertable('{self.username}', '{self.email}', '{self.password}')"


class logintable(db.Model):
  #database table name logintable
  id = db.Column(db.Integer, primary_key=True)
  logname = db.Column(db.String(20), unique=True, nullable=False)
  logpass = db.Column(db.String(60), nullable=False)
  logint = db.Column(db.Integer())
  logbool = db.Column(db.Boolean, default=False)
  
  def __repr__(self):
    return f"logintable('{self.logname}', '{self.logpass}', '{self.logint}', '{self.logbool}')"    

#new code added to make sure table is created
db.create_all()

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        if request.method == 'POST' and form.validate():
            user_a = User(username=form.username.data, email=form.email.data, password=form.password.data)
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

@app.route("/login",methods=['GET', 'POST'])
def login():
    lform = LoginForm(request.form)
    if lform.validate_on_submit():
        if request.method == 'POST' and lform.validate():
            aa = logintable( logname=lform.logname.data,  
                            logpass=lform.logpass.data, logint=lform.logint.data, 
                            logbool=lform.b)
            db.session.add(aa)
            db.session.commit()
            flash(f'Login created for {lform.logname.data}!', 'success')
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=lform)


if __name__ == '__main__':               # this should always be at the end avoids the need for environment variables
    app.run(debug=True, host="0.0.0.0")

#to run set environment variable:export FLASK_APP=demo unless you can use the command above
