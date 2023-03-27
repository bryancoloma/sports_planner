from telnetlib import LOGOUT
from flask_app import app
from flask import Flask,render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.event import Event


@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/create_event')
def create_event():
    if "user_id" not in session:
        return redirect('/')
    return render_template('/create_event.html')

@app.route('/view_event/<int:event_id>')
def view_event(event_id):
    if "user_id" not in session:
        return redirect('/')
    return render_template('/event_details.html', event=Event.get_event_by_id(event_id))

@app.route('/edit_event/<int:event_id>')
def edit_event(event_id):
    if "user_id" not in session:
        return redirect('/')
    return render_template('/event_update.html', event=Event.get_event_by_id(event_id))

@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    if "user_id" not in session:
        return redirect('/')
    print("calling delete event")
    Event.delete_event(event_id)
    return redirect('/')

@app.route('/submit_event',methods=['POST'])
def submit_event():
    print(request.form)
    # validate the form here ...
    # create event
    if not Event.validate_event(request.form):
        return redirect('/create_event')
    data = {
        "name": request.form["name"],
        "under" : request.form["under"],
        "description" : request.form["desc"],
        "instructions" : request.form["inst"],
        "date_made" : request.form["datecooked"],
        "user_id" : session["user_id"]
    }
    # Call the save @classmethod on User
    Event.create_event(data)
    return redirect('/')

@app.route('/submit_edited_event/<int:event_id>',methods=['POST'])
def submit_edited_event(event_id):
    # validate the form here ...
    # create event
    if not Event.validate_event(request.form):
        print("validation didn't work")
        return redirect('/edit_event/'+event_id)
    data = {
        "id": event_id,
        "name": request.form["name"],
        "under" : request.form["under"],
        "description" : request.form["desc"],
        "instructions" : request.form["inst"],
        "date_made" : request.form["datecooked"],
        "user_id" : session["user_id"]
    }
    # Call the save @classmethod on User
    Event.edit_event(data)
    return redirect('/events')