from re import I
from tabnanny import check
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Different URLS to find
auth = Blueprint('auth', __name__)

# different routes & their URLS, best practice to name function after route
# By default can only use GET requests, but with methods=[], added POST as an option
@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':   
      email = request.form.get('email')
      password = request.form.get('password')

      # looking for specific entry in database
      # looks by specific column or field etc
      user = User.query.filter_by(email=email).first()
      if user:
         if check_password_hash(user.password, password):
            flash('Logged in succesfully!', category='success')
            # remembers user is logged in until sesssion is cleared
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
         else:
            flash('Incorrect password, try again.', category='error')
      else:
         flash('Email does not exist', category='error')

  # text="" text is the variable, quotes is value, can be passed to page
  return render_template("login.html", user=current_user)

# make sure cannot access page unless user is logged in
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
   logout_user()
   return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
   email = request.form.get('email')
   firstName = request.form.get('firstName')
   password1 = request.form.get('password1')
   password2 = request.form.get('password2')

   user = User.query.filter_by(email=email).first()
   if user:
      flash('Email already exists.', category='error')
   elif len(email) < 4:
      flash('Email must be greater than 3 characters', category='error')
   elif len(firstName) < 2:
      flash('First name must be greater than 1 character', category='error')
   elif password1 != password2:
      flash('Passwords don\'t match', category='error')
   elif len(password1) < 7:
      flash('Password must be at least 7 characters', category='error')
   else:
      # make new user
      new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
      #Add new user to database
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True)
      flash('Account created!', category='success')
      # redirect to homepage and signed in
      # views is blueprint, home is function. finding url that maps to function
      return redirect(url_for('views.home'))

  return render_template("sign-up.html", user=current_user)