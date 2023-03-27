import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Event:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.date = data['date']
        self.time = data['time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.messages = []

    @staticmethod
    def validate_event(event):
        is_valid = True # we assume this is true
        if len(event['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(event['location']) < 3:
            flash("Location must be at least 2 characters.")
            is_valid = False
        if len(event['date']) < 1:
            flash("Date must be selected.")
            is_valid = False
        if len(event['time']) < 1:
            flash("Time must be selected.")
            is_valid = False
        return is_valid

    @classmethod
    def create_event(cls,data):
        query = "INSERT INTO events ( name ,location, date, time, user_id ) VALUES ( %(name)s ,%(location)s, %(date)s ,%(time)s , %(user_id)s );"
        event_id = connectToMySQL('sports_planner').query_db(query,data)
        print(event_id)
        return event_id

    @classmethod
    def edit_event(cls,data):
        print("inside edit event")
        query = "UPDATE events SET name=%(name)s, location=%(location)s, date= %(date)s, time=%(time)s  WHERE id=%(id)s;"
        print(query)
        event_id=connectToMySQL('sports_planner').query_db(query,data)
        return event_id
    
    @classmethod
    def delete_event(cls,event_id):
        print("inside delete event")
        data = {"id": event_id}
        query = "DELETE from events WHERE id=%(id)s;"
        print(query)
        event_id=connectToMySQL('sports_planner').query_db(query,data)
        return event_id


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM events;"
        events = []
        results = connectToMySQL('sports_planner').query_db(query)
        for row in results:
            events.append(cls(row))
        return events
    
    @classmethod
    def get_event_by_id(cls,event_id):
        data = {"id": event_id}
        query = "SELECT * FROM events JOIN users on users.id = events.user_id where events.id=%(id)s;"
        result = connectToMySQL('sports_planner').query_db(query,data)
        print("Event info")
        print(result)
        row=result[0]
        # Create a Event class instance from the information 
        one_event = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
        one_event_info = {
            # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
            "id": row['users.id'], 
            "first_name": row['first_name'],
            "last_name": row['last_name'],
            "email": row['email'],
            "password": row['password'],
            "created_at": row['users.created_at'],
            "updated_at": row['users.updated_at']
        }
            # Create the User class instance that's in the user.py model file
        one_event.creator= user.User(one_event_info)
            
        return one_event

    @classmethod
    def get_all_by_user(cls,user_id):
        data = {"id": user_id}
        query = "SELECT * FROM events JOIN users on users.id = events.user_id where user_id=%(id)s;"
        results = connectToMySQL('sports_planner').query_db(query,data)
        print(results)
        all_events = []
        for row in results:
        # Create a Event class instance from the information from each db row
            one_event = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_event_author_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }

            # Create the User class instance that's in the user.py model file
            author = user.User(one_event_author_info)
            # Associate the event class instance with the User class instance by filling in the empty creator attribute in event the class
            one_event.creator = author
            # Append the event containing the associated User to your list of events
            all_events.append(one_event)   
        return all_events

    @classmethod
    def get_all_by_user_today(cls,user_id):
        data = {"id": user_id}
        query = "SELECT * FROM events JOIN users on users.id = events.user_id where user_id=%(id)s and events.date=CURDATE();"
        results = connectToMySQL('sports_planner').query_db(query,data)
        print("These are the events")
        print(results)
        all_events = []
        print("This is the  lenght")
        print(len(results))
        for row in results:
        # Create a Event class instance from the information from each db row
            one_event = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_event_author_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }

            # Create the User class instance that's in the user.py model file
            author = user.User(one_event_author_info)
            # Associate the event class instance with the User class instance by filling in the empty creator attribute in event the class
            one_event.creator = author
            # Append the event containing the associated User to your list of events
            all_events.append(one_event)
        return all_events