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
        return render_template("login.html")
    if session['user'] > 0:
        user_id = session['user']
        print("found session")
        return redirect('/dashboard')
    else:
        return render_template("login.html")
        

@app.route('/login', methods=['POST']) #already have an account button that directs to login page
def login():
    # data = {"email" : request.form["email"]}
    if not (User.login_validation(request.form)):
        return redirect('/')
    # if not user_in_db: #redirects to login page if email not in db
    #     flash('Invalid Email or Password')
    #     print('Invalid Email ')
    #     return redirect('/')
    # if not bcrypt.check_password_hash(user_in_db.password, request.form['password']): #redirects to login page if password is wrong
    #     flash('Invalid Email or Password')
    #     print('Invalid Password')
    #     return redirect('/')
    # print('valid')
    user_in_db = User.get_by_email(request.form['email'])
    session['user'] = user_in_db.id #stores user id in session
    user_id = user_in_db.id #collects user id into variable to send through url
    return redirect('/dashboard')

@app.route('/register')
def registerAccount():
    return render_template('register.html')

@app.route('/existingaccount') #already have an account button that directs to login page
def existingAccount():
    return render_template('loginform.html')

@app.route('/createaccount', methods=['POST']) #route for recieving form data and creating user
def createAccount():
    print(request.form)
    
    
    if not User.register_validation(request.form): #validate user otherwise redirect to registration page
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) #hash password
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    } #reset data to be stored in db

    user_id = User.register_user(data) #create user
    session['user'] = user_id #set session user id
    return redirect('/dashboard')


# @app.route('/dashboard/<int:id>') #when user logs in, display dashboard
# def dashboard(id):
#     if session['user'] != id: #checks url to see if the user logged in is the same as the account being accesses
#         return redirect('/logout') #if not, logs out the user
#     user = User.get_user(id) #gets user by id so the dashboard can access user data
#     todaysEvents = Event.get_all_by_user_today(id) #gets todays events that user is attending
#     allEvents = Event.get_future_events_by_user(id) #gets all events to display in dash
#     return render_template('index.html', user = user, allEvents = allEvents, todaysEvents = todaysEvents)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    logged_user = User.get_user_with_events(session['user'])
    return render_template('index.html', user = logged_user)



'''@app.route('/user_account')
def userInfo():
    id = session['user']
    user = User.get_user(id)
    events = Event.get_all_by_user(id)
    events_today = Event.get_all_by_user_today(id)
    return render_template('account.html', user = user, events = events, events_today = events_today)
    '''

@app.route('/user/<int:id>')
def user_details(id):
    user = User.get_user(id)
    events = Event.get_all_by_user(id)
    return render_template('user_details.html', user = user, events = events)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
