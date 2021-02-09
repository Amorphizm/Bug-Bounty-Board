from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        psswd = request.form.get('psswd')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.passwd, psswd):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.projects'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully. See ya later!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('first_name')
        psswd = request.form.get('psswd_1')
        psswd_conf = request.form.get('psswd_2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstname) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif psswd != psswd_conf:
            flash('Passwords do not match.', category='error') 
        elif len(psswd) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            new_user = User(email=email, f_name=firstname, passwd=generate_password_hash(psswd, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.projects'))
        
    return render_template("sign_up.html", user=current_user)
