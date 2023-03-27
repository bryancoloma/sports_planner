from flask_app.config.sqlconnection import connectToMySQL
from flask_app import app
from flask import flash
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

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

    @classmethod
    def register_user(cls, data):
        query ="""INSERT INTO users (first_name, last_name, email, password) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL(cls.DB).query_db(query, data)
    
    # the following two methods are validation for register_user
    @classmethod
    def register_validation(cls, form):
        is_valid = True
        # check for blank inputs
        for field in form:
            if len(form[field]) < 1:
                is_valid = False
                message = f"{field} is required"
                make_pretty = message.maketrans("_", " ")
                flash(message.translate(make_pretty), "register")
        # check if passwords match
        if form['password'] != form['confirm_password']:
            is_valid = False
            flash("passwords do not match", "register")
        # check min length of 8 for password
        if len(form['password']) > 0 and len(form['password'] <= 7):
            is_valid = False
            flash("password must be at least 8 characters", "register")
        # check email format
        if not EMAIL_REGEX.match(form['email']) and len(form['email']) > 0:
            is_valid = False
            flash("email is invalid", "register")
        # check if email has been used already
        optional_user = cls.find_by_email(form['email'])
        if not(optional_user == False):
            is_valid = False
            flash("email already used, please log in", "register")
        return is_valid
    
    @classmethod
    def find_by_email(cls, email):
        data = {
            "email": email
        }
        query = "SELECT * FROM users WHERE users.email = %(email)s LIMIT 1;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results