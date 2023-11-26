from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Alex!'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    app.app_context().push()


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database()

    login_maneger = LoginManager()
    login_maneger.login_view = 'auth.login'
    login_maneger.init_app(app)

    @login_maneger.user_loader
    def load_user(id):
        return User.query.get(int(id))

    print('app running')
    
    return app

def create_database():
    if not path.exists('instance/database.db'):
        db.create_all()
        print('database created')