# Database models
from . import db
# custom class we can inherit to give user object something for Flasklogin
from flask_login import UserMixin
from sqlalchemy.sql import func

# db.Model is telling database the format of the data. for consistency
class Note(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   data = db.Column(db.String(10000))
   # automatically add date for us. get current date with func
   date = db.Column(db.DateTime(timezone = True), default=func.now())
   # for every single note, we wanna store ID of user 
   # foreign key enforces valid user for object
   # foreign key -- user.id references the User class-- its lowercase bc sql reads lower
   userID = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(150), unique=True)
   password = db.Column(db.String(150))
   firstName = db.Column(db.String(150))
   # tell program to do magic and everytime create note, add note ID to user relationship
   # access all notes user created from notes field. 
   notes = db.relationship('Note')
