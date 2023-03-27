from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
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

    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if not TEXT_REGEX.match(user['first_name']): 
            flash("Only letters accepted!")
            is_valid = False
        if not TEXT_REGEX.match(user['last_name']): 
            flash("Only letters accepted!")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 2 characters.")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords do not match!.")
            is_valid = False
        #IF EMAIL IS IN DATABASE
        return is_valid

    @classmethod
    def register_user(cls, data):
        query ="""INSERT INTO users (first_name, last_name, email, password) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def find_by_email(cls, email):
        data = {
            "email": email
        }
        query = "SELECT * FROM users WHERE users.email = %(email)s LIMIT 1;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def login_validation(cls, form):
        is_valid = True
        if not EMAIL_REGEX.match(form['email']):
            is_valid = False
            flash("invalid email/password", "login")
        return is_valid
    
    @classmethod
    def get_user(cls, user_id):
        data = {
            "user_id": user_id
        }
        query = "SELECT * FROM users WHERE users.id = %(user_id)s LIMIT 1;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])