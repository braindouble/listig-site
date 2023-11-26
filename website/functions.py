from .models import User, Item, List
from . import db
from flask import Flask, redirect, session, render_template, Blueprint, request, flash, url_for
from datetime import datetime
from flask_login import current_user, login_required, login_user, logout_user 
from werkzeug.security import check_password_hash, generate_password_hash



def add_new_item(data, current_list):
    new_item = Item(data=data, user_id=current_user.id, list_id=current_list.id)
    print(new_item)
    db.session.add(new_item)
    db.session.commit()


def share_with(shared_user, lister):
        if shared_user:
            print(shared_user)
            sharing = User.query.filter_by(username=shared_user).first()
            print('.................................')

            if sharing:
                now_list = List.query.filter_by(name=lister).first()
                user_extra = User.query.filter_by(username=shared_user).first()
                now_list.users.append(user_extra)
                db.session.commit()
                    
                print('user is available')
                return redirect(url_for('views.list'))
            else:
                flash(f'no user called {shared_user}', category='error')
                return render_template('list.html', user=current_user)
            

def get_latest_notes(user_id, num_notes=10):
    latest_notes = Item.query.filter_by(user_id=user_id).order_by(Item.date.desc()).limit(num_notes).first()
    return latest_notes


def return_def(file, value1=None, value2=None, value3=None):
    return render_template(file, value1=value1, value2=value2, value3=value3)