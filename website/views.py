from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# Blueprint of applicaion -- routes inside, URLS to find
# Easier to name same thing as file
views = Blueprint('views', __name__)

# decorate, define route, when hit route: run function
# cannot view page unless logged in
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
   if request.method == 'POST':
      note = request.form.get('note')

      if len(note) < 1:
         flash('Note is too short!', category='error')
      else:
         new_note = Note(data=note, userID=current_user.id)
         db.session.add(new_note)
         db.session.commit()
         flash('Note added!', category='success')
    # this function will run whenever we go to /route
    # in template, reference current user and check if authenticated
   return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
   note = json.loads(request.data)
   noteId = note['noteId']
   note = Note.query.get(noteId)
   if note:
      if note.userID == current_user.id:
         db.session.delete(note)
         db.session.commit()
   #turn into json object u can return. just gotta return something
   return jsonify({})