from flask import Flask, redirect, render_template, Blueprint, request, flash, url_for
from .models import User
from . import db
from flask_login import current_user, login_required, login_user, logout_user 
from werkzeug.security import check_password_hash, generate_password_hash
from .functions import return_def

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        email = request.form.get('signup_email')
        username = request.form.get('signup_username')
        password = request.form.get('signup_password')
        password_check = request.form.get('signup_password_check')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('email already exists', category='error')
            return return_def('signup.html', email, username, password)
        elif len(username) < 3:
            flash('username must be at least 3 characters', category='error')
            return return_def('signup.html', email, username, password)
        elif len(password) < 5:
            flash('password must be at least 5 characters', category='error')
            return return_def('signup.html', email, username, password)
        elif password != password_check:
            flash('passwords dis not match', category='error')
            return return_def('signup.html', email, username, password)
        if '/' in username:
            flash("username can not containt '/'", category='error')
            return return_def('signup.html', email, username, password)
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('acount created', category='succes')
            return redirect(url_for('views.list'))


    return render_template('signup.html')

@auth.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form.get('login_email')
        password = request.form.get('login_password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.list'))
        else:
            flash('email does not exist', category='error')

    return render_template('login.html')


@auth.route('/acount', methods=['POST', 'GET'])
@login_required
def acount():

    user = User.query.filter_by(email=current_user.email).first()

    if not user:
        flash('create a acount', category='error', redirect='/signup')
        return redirect(url_for('auth.signup'))
    else:      
        username = user.username
        email = user.email
        user_lists = user.lists

        contacts = []

        for contact_person in user_lists:
            contacts.extend(contact_person.users)

        all_contacts = []

        for person in contacts:
            username_contact = User.query.filter_by(id=person.id).first()
            all_contacts.append(username_contact.username.lower())
            fix_list = list(set(all_contacts))
            html_contact = ", ".join(fix_list)


    return render_template('acount.html', username=username, email=email, user_lists=user_lists, contacts=html_contact)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))