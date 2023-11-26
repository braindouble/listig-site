from flask import Flask, redirect, session, render_template, Blueprint, request, flash, url_for
from .models import User, Item, List
from . import db
from datetime import datetime
from flask_login import current_user, login_required, login_user, logout_user 
from werkzeug.security import check_password_hash, generate_password_hash
from .functions import add_new_item, share_with, get_latest_notes

views = Blueprint('views', __name__)


@views.route('/')
def homepage():
    return render_template('home.html')



@views.route('/list', methods=['POST', 'GET'])
@login_required
def list():
    current_date = datetime.now().date()
    print(current_date)
    
    none_note = Item.query.filter_by(user_id=current_user.id).first()
    if none_note:
        last_active = get_latest_notes(current_user.id)
        late_id = last_active.list_id
        done_late = List.query.filter_by(id=late_id).first()
        print(done_late.name)

        if done_late  in current_user.lists:
                current_user.lists
                current_user.lists.remove(done_late)
                current_user.lists.insert(0, done_late)

    list_name = 'enter the name of your list'
    shared_user = 'share list with(optional)'

    if request.method == 'POST':
        list_name = request.form.get('list_name')
        shared_user = request.form.get('share_list')
        print('post received')

        existing_list = List.query.filter_by(name=list_name).filter(List.users.any(id=current_user.id)).first()

        if existing_list:
            flash('list already exists', category='error')
            return render_template('list.html', user=current_user, current_date=current_date, placeholder1=list_name, placeholder2=shared_user)
        elif '/' in list_name:
            flash("list name can't containt '/'", category='error')
            return render_template('list.html', user=current_user, current_date=current_date, placeholder1=list_name, placeholder2=shared_user)
        else:
            new_list = List(name=list_name)
            db.session.add(new_list)
            db.session.commit()

            user1 = User.query.filter_by(username=current_user.username).first()
            new_list.users.append(user1)


            if shared_user:
                print(shared_user)
                sharing = User.query.filter_by(username=shared_user).first()
                print('.................................')

                if sharing:
                    user2 = User.query.filter_by(username=shared_user).first()
                    new_list.users.append(user2)
                    db.session.commit()
        
                    flash("List created!", category='succes')

                    return render_template('list.html', user=current_user, current_date=current_date, placeholder1='enter the name of your list', placeholder2='share list with(optional)')
                else:
                    flash(f'no user called {shared_user}', category='error')
                    return render_template('list.html', user=current_user, current_date=current_date, placeholder1=list_name, placeholder2=shared_user)
            else:
                new_list.users.append(current_user)
                db.session.commit()

                flash("List created!", category='succes')
            
        return render_template('list.html', user=current_user, current_date=current_date, placeholder1='enter the name of your list', placeholder2='share list with(optional)')

    return render_template('list.html', user=current_user, current_date=current_date, placeholder1='enter the name of your list', placeholder2='share list with(optional)')






@views.route('/<lister>', methods=['POST', 'GET'])
@login_required
def notes(lister):
    current_list = List.query.filter_by(name=lister).first()
    print(current_list)


    if request.method == 'POST':
        data = request.form.get('item')
        shared_user = request.form.get('share')
        important = request.form.get('check1')
        data_lower = data.lower()
    
        if len(data) > 15:
            flash('item must be less then 15 characters long', category='error')

        else:
            if len(data) == 0 and len(shared_user) != 0:
                share_with(shared_user, lister)
            else:
                add_new_item(data, current_list)
                share_with(shared_user, lister)

    return render_template('list_edit.html', user=current_user, current_list=current_list.items, User=User, listing=current_list)





@views.route('/example')
def example():
    return render_template('list.html')