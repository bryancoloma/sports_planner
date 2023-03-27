from flask_app.config.sqlconnection import connectToMySQL
from flask_app import app
from flask import flash

class Event:
    DB = "sports_planner"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.date = data['date']
        self.time = data['time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.host = None