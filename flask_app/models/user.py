from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import event
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
TEXT_REGEX = re.compile(r'^[a-zA-Z]+$') 

class User:
    DB = "sports_planner"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.events = []

    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        user_id = connectToMySQL(cls.DB).query_db(query, data)
        return user_id
    
    # the following two methods are validation for register_user    
    @classmethod
    def register_validation(cls,form):
        is_valid = True
        # check for blank inputs
        for field in form:
            if len(form[field]) < 1:
                is_valid = False
                message = f"{field} is required"
                make_pretty = message.maketrans("_", " ")
                flash(message.translate(make_pretty), "register")
        # check if passwords match
        if form['password'] != form['confirm']:
            is_valid = False
            print("passwords do not match")
            flash("passwords do not match", "register")
        # check min length of 8 for password
        if len(form['password']) > 0 and len(form['password']) < 8:
            is_valid = False
            print("LENGTH")
            flash("password must be at least 8 characters", "register")
        # check email format
        if not EMAIL_REGEX.match(form['email']) and len(form['email']) > 0:
            is_valid = False
            print("email")
            flash("email is invalid", "register")
        # check if email has been used already
        emails = cls.get_emails()
        for each_email in emails:
            if each_email['email'] == form['email']:
                flash('email already used, please login', 'register')
                is_valid = False
        return is_valid
    
    @classmethod
    def find_by_email(cls, email):
        data = {
            "email": email
        }
        query = "SELECT * FROM users WHERE users.email = %(email)s LIMIT 1;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def email_validation(cls, form):
        is_valid = True
        if not EMAIL_REGEX.match(form['email']):
            is_valid = False
            flash("invalid email/password", "login")
        return is_valid
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        users_from_db = connectToMySQL(cls.DB).query_db(query)
        users = []
        for each_row in users_from_db:
            users.append(cls(each_row))
        return users
    
    @classmethod
    def get_emails(cls):
        query = "SELECT email FROM users;"
        emails = connectToMySQL(cls.DB).query_db(query)
        return emails

    @classmethod
    def get_user(cls, user_id):
        data = {
            "user_id": user_id
        }
        query = "SELECT * FROM users WHERE users.id = %(user_id)s LIMIT 1;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, form):
        data = {
            "email": form['email']
            }
        query = "SELECT * FROM users WHERE email= %(email)s LIMIT 1;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) == 0:
            return False
        return cls(results[0])

"""   @classmethod
    def get_user_with_events(cls, user_id):
        data = {
            "user_id": user_id
        }
        query = "SELECT * FROM users JOIN events ON events.user_id = users.id WHERE users.id = %(user_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        user = cls(results[0])
        for row in results:
            event_info = {
                "id": row['events.id'],
                "name": row['name'],
                "location": row['location'],
                "date": row['date'],
                "time": row['time'],
                "created_at": row['events.created_at'],
                "updated_at": row['events.updated_at']
            }
            one_event = event.Event(event_info)
            user.events.append(one_event)
        return user"""