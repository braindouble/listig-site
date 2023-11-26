from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

user_lists = db.Table('user_lists',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('list_id', db.Integer, db.ForeignKey('list.id'))
)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(17))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    items = db.relationship('Item')
    lists = db.relationship('List', secondary=user_lists, back_populates='users')


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    items = db.relationship('Item')
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    users = db.relationship('User', secondary=user_lists, back_populates='lists')