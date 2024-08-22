from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

def debug_config():
    return True

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
    app.secret_key = 'KEY'

    from views import config_views
    config_views(app, db, Bcrypt(app))
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    from models import User

    @login_manager.user_loader
    def get_uid(id):
        return User.query.get(id)
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('login', next=url_for('home')))
    
    db.init_app(app)
    migrate = Migrate(app, db)

    return app