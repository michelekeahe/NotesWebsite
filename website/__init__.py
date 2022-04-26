from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager

# Define database
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
   # Initialize flask
   app = Flask(__name__)
   # Secret key for app. In production, NEVER SHARE
   app.config['SECRET_KEY'] = 'mysecretkey' 
   # Database is stored at this* location in f--DB_NAME
   # f{string} - if f, anything in {} will return as string
   app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

   db.init_app(app)

   # import blueprints
   from .views import views
   from .auth import auth
   # If you don't want prefix, keep it at '/'
   app.register_blueprint(views, url_prefix='/')
   app.register_blueprint(auth, url_prefix='/')

   # need to make sure we load file before initialize and create database
   from .models import User, Note
   create_database(app)
   
   # where to redirect if not logged in
   login_manager = LoginManager()
   login_manager.login_view = 'auth.login'
   login_manager.init_app(app)

   # Tell flask how to load user
   @login_manager.user_loader
   def load_user(id):
      # similar to filter_by but defaults to primary key instead
      return User.query.get(int(id))
      
   return app

def create_database(app):
   if not path.exists('website/' + DB_NAME):
      db.create_all(app=app)
      print('Created Database!')
