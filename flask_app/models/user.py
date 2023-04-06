from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import event
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash
import datetime
today = datetime.date.today()
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
        self.events_today = []
        self.future_events = []

    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        user_id = connectToMySQL(cls.DB).query_db(query, data)
        return user_id
    
    @classmethod
    def register_validation(cls, form):
        is_valid = True
        # check if email has been used already
        all_emails = cls.get_emails()
        for email in all_emails:
            if email['email'] == form['email']:
                is_valid = False
                flash('email already used, please login')
                return is_valid
        # check for blank inputs
        for field in form:
            if len(form[field]) < 1:
                is_valid = False
                message = f"{field} is required"
                make_pretty = message.maketrans("_", " ")
                flash(message.translate(make_pretty))
        # check email format
        if not cls.email_validation(form['email']) and len(form['email']) > 0:
            is_valid = False
            flash("email is invalid")
        # check min length of 8 for password
        if len(form['password']) > 0 and len(form['password']) < 8:
            is_valid = False
            flash("password must be at least 8 characters")
            return is_valid
        # check if passwords match
        if form['password'] != form['confirm']:
            is_valid = False
            flash("passwords do not match")
        return is_valid
        
    @classmethod
    def get_emails(cls):
        query = "SELECT email FROM users;"
        all_emails = connectToMySQL(cls.DB).query_db(query)
        return all_emails

    @classmethod
    def get_user(cls, user_id):
        data = {
            "user_id": user_id
        }
        query = "SELECT * FROM users WHERE users.id = %(user_id)s LIMIT 1;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def login_validation(cls, form):
        data = {
            "email": form['email'],
            "password": form['password']
        }
        is_valid = True
        if not cls.email_validation(data['email']):
            is_valid = False
            flash("invalid email/password")
            return is_valid
        optional_user = cls.get_by_email(data['email'])
        if not optional_user:
            is_valid = False
            flash("email not found, please register")
            return is_valid
        if not bcrypt.check_password_hash(optional_user.password, data['password']):
            is_valid = False
            flash("invalid email/password")
            return is_valid
        return is_valid
    
    @classmethod
    def get_by_email(cls, email):
        data = {
            "email": email
            }
        query = "SELECT * FROM users WHERE email= %(email)s LIMIT 1;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) == 0:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_with_events(cls, user_id):
        data = {
            "user_id": user_id
        }
        query = """SELECT * FROM users
                LEFT JOIN events ON events.user_id = users.id
                LEFT JOIN players ON players.event_id = events.id
                WHERE events.date >= CURDATE() AND users.id = %(user_id)s OR players.user_id = %(user_id)s
                ORDER BY date ASC LIMIT 10;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) == 0:
            return cls.get_user(user_id)
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
            if today.strftime('%Y-%m-%d') == str(one_event.date):
                user.events_today.append(one_event)
            # elif today.strftime('%Y-%m-%d') < str(one_event.date):
            else:  
                user.future_events.append(one_event)
        return user

    @staticmethod
    def email_validation(email):
        is_valid = True
        if not EMAIL_REGEX.match(email):
            is_valid = False
        return is_valid