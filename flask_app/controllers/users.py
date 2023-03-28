import re
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/') #main, checks if user is already logged in, if not, directs to registration page
def main():
    if not session.get('user'):
        return render_template("registration.html")
    if session['user'] > 0:
        return redirect('/index')
    else:
        return render_template("registration.html")
    
@app.route('/register')
def register():
    return redirect('/')

@app.route('/login') #already have an account button that directs to login page
def existingAccount():
    if not session.get('user'):
        return render_template('loginform.html')
    if session['user'] == 0:
        return render_template('loginform.html')
    if session['user'] > 0:
        return redirect('/index')

@app.route('/login_user', methods=['POST']) #login route, collects user data by email input and checks against database
def login():
    email = request.form['email']
    user_in_db = User.find_by_email(email)
    if not user_in_db: #redirects to login page if email not in db
        flash('Invalid Email or Password')
        return redirect('/existingaccount')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']): #redirects to login page if password is wrong
        flash('Invalid Email or Password')
        return redirect('/existingaccount')
    session['user'] = user_in_db.id #stores user id in session
    return redirect('/index')

@app.route('/index') #when user logs in, display dashboard
def index():
    id = session['user']
    user = User.get_user(id) #gets user by id so the dashboard can access user data
    events = Event.getAllEvents() #gets all events to display in dash
    todaysEvents = Event.getEventsByUserToday(id) #gets todays events that user is attending
    return render_template('dashboard.html', user = user, events = events, todaysEvents = todaysEvents)

@app.route('/register_user', methods=['POST']) #route for recieving form data and creating user
def createUser():
    form = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "confirm_password" : request.form['confirm']
    } #set initial data to be validated
    if not User.register_validation(form): #validate user otherwise redirect to registration page
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) #hash password
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    } #reset data to be stored in db
    User.register_user(data) #create user
    return redirect('/login')

@app.route('/user_account')
def userInfo():
    id = session['user']
    user = User.get_user(id)
    events = Event.get_all_by_user(id)
    events_today = Event.get_all_by_user_today(id)
    return render_template('account.html', user = user, events = events, events_today = events_today)

@app.route('/user/<int:id>')
def user_details(id):
    user = User.get_user(id)
    events = Event.get_all_by_user(id)
    return render_template('user_details.html', user = user, events = events)

@app.route('/log_out')
def logout():
    session['user'] = 0
    return redirect('/')
